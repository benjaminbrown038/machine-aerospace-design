"""Small, transparent analytical models. See each tier README for assumptions."""
import math


def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("{} must be a number".format(name))
    if not math.isfinite(value) or (positive and value <= 0):
        raise ValueError("{} must be finite{}".format(name, " and positive" if positive else ""))
    return value


def get(c, key, positive=False):
    return number(c[key], key, positive)


def factor(c):
    sf = get(c, "design_factor", True)
    if sf < 1:
        raise ValueError("design_factor must be at least 1")
    return sf


def check(demand, allowable):
    """A zero demand passes; its undefined/infinite reserve is represented by null."""
    return {"demand": demand, "allowable": allowable,
            "utilization": demand / allowable,
            "margin": allowable / demand - 1 if demand > 0 else None,
            "passes": demand <= allowable}


def material(c):
    m = c["material"]
    for key in ("E_Pa", "yield_Pa", "density_kg_m3"):
        get(m, key, True)
    return m


def cantilever(c):
    """Uniform rectangular cantilever under one transverse tip force."""
    m = material(c)
    length, width, height = [get(c, k, True) for k in ("length_m", "width_m", "height_m")]
    force = get(c, "tip_force_N")
    sf = factor(c)
    inertia = width * height ** 3 / 12
    stress = abs(force) * length * height / (2 * inertia)
    displacement = force * length ** 3 / (3 * m["E_Pa"] * inertia)
    checks = {
        "bending_Pa": check(stress, m["yield_Pa"] / sf),
        "tip_deflection_m": check(abs(displacement), get(c, "max_deflection_m", True)),
    }
    # These are explicit screening rules for this teaching model, not universal limits.
    valid = length / height >= 10 and abs(displacement) / length <= 0.05
    profile = [{"x_m": length * i / 40,
                "deflection_m": force * (length * i / 40) ** 2 * (3 * length - length * i / 40)
                / (6 * m["E_Pa"] * inertia)} for i in range(41)]
    return {"model": "cantilever", "I_m4": inertia,
            "root_bending_stress_Pa": stress, "tip_deflection_m": displacement,
            "mass_kg": m["density_kg_m3"] * length * width * height,
            "length_height_ratio": length / height, "model_screen_passes": valid,
            "checks": checks, "passes": valid and all(x["passes"] for x in checks.values()),
            "profile": profile}


def shaft(c):
    """Nominal surface stress and twist of a solid circular shaft."""
    m = material(c)
    diameter, length = [get(c, k, True) for k in ("diameter_m", "length_m")]
    shear_modulus = get(m, "G_Pa", True)
    moment, torque = get(c, "bending_moment_Nm"), get(c, "torque_Nm")
    sf = factor(c)
    polar = math.pi * diameter ** 4 / 32
    normal = 32 * abs(moment) / (math.pi * diameter ** 3)
    shear = 16 * abs(torque) / (math.pi * diameter ** 3)
    equivalent = math.hypot(normal, math.sqrt(3) * shear)
    twist = torque * length / (shear_modulus * polar)
    checks = {"von_mises_Pa": check(equivalent, m["yield_Pa"] / sf),
              "twist_rad": check(abs(twist), get(c, "max_twist_rad", True))}
    return {"model": "shaft", "J_m4": polar, "bending_stress_Pa": normal,
            "torsional_shear_Pa": shear, "von_mises_Pa": equivalent,
            "twist_rad": twist, "twist_deg": math.degrees(twist),
            "mass_kg": m["density_kg_m3"] * math.pi * diameter ** 2 * length / 4,
            "checks": checks, "passes": all(x["passes"] for x in checks.values())}


def point(value, name):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("{} must contain x and y".format(name))
    return tuple(number(v, name) for v in value)


def bolt_group(c):
    """Equal-stiffness bolts sharing force and moment in the joint plane."""
    pts = [point(p, "bolt_xy_m") for p in c["bolt_xy_m"]]
    if len(pts) < 2 or len(set(pts)) != len(pts):
        raise ValueError("Use at least two distinct bolt positions")
    n = len(pts)
    cx, cy = sum(x for x, y in pts) / n, sum(y for x, y in pts) / n
    relative = [(x - cx, y - cy) for x, y in pts]
    group_j = sum(x*x + y*y for x, y in relative)
    if group_j <= 0:
        raise ValueError("Bolt group must have a nonzero spread")
    fx, fy = point(c["force_xy_N"], "force_xy_N")
    ax, ay = point(c["load_point_xy_m"], "load_point_xy_m")
    moment = get(c, "free_moment_Nm") + (ax - cx) * fy - (ay - cy) * fx
    diameter, thick = get(c, "bolt_diameter_m", True), get(c, "plate_thickness_m", True)
    sf = factor(c)
    shear_allow = get(c, "bolt_shear_strength_Pa", True) / sf
    bearing_allow = get(c, "plate_bearing_strength_Pa", True) / sf
    area = math.pi * diameter ** 2 / 4
    rows = []
    for i, (x, y) in enumerate(relative):
        bx, by = fx / n - moment * y / group_j, fy / n + moment * x / group_j
        load = math.hypot(bx, by)
        shear, bearing = load / area, load / (diameter * thick)
        rows.append({"bolt": i + 1, "x_m": pts[i][0], "y_m": pts[i][1],
                     "force_x_N": bx, "force_y_N": by, "force_N": load,
                     "shear_Pa": shear, "bearing_Pa": bearing,
                     "shear_utilization": shear / shear_allow,
                     "bearing_utilization": bearing / bearing_allow})
    checks = {"bolt_shear_Pa": check(max(r["shear_Pa"] for r in rows), shear_allow),
              "plate_bearing_Pa": check(max(r["bearing_Pa"] for r in rows), bearing_allow)}
    return {"model": "bolt_group", "centroid_xy_m": [cx, cy], "moment_at_centroid_Nm": moment,
            "sum_radius_squared_m2": group_j, "bolts": rows, "checks": checks,
            "passes": all(x["passes"] for x in checks.values())}


def actuator(c):
    """Planar arm with a two-force actuator from a fixed anchor to the arm tip."""
    radius = get(c, "arm_radius_m", True)
    ax, ay = point(c["anchor_xy_m"], "anchor_xy_m")
    start, stop = get(c, "start_angle_deg"), get(c, "stop_angle_deg")
    samples = c["samples"]
    if isinstance(samples, bool) or not isinstance(samples, int) or not 2 <= samples <= 10000:
        raise ValueError("samples must be an integer between 2 and 10000")
    if stop <= start or stop - start > 360:
        raise ValueError("Use an increasing angle range spanning at most 360 degrees")
    if math.hypot(ax, ay) <= 1e-12:
        raise ValueError("An anchor at the arm pivot has no moment arm")
    moment = get(c, "resisting_moment_Nm")
    sf = factor(c)
    capacity = get(c, "actuator_force_capacity_N", True)
    travel = get(c, "available_stroke_m", True)
    angles = [start + (stop - start) * i / (samples - 1) for i in range(samples)]
    # Include collinear positions exactly: a coarse grid must not hide a dead center.
    base = math.degrees(math.atan2(ay, ax))
    first = math.ceil((start - base) / 180)
    last = math.floor((stop - base) / 180)
    angles += [base + 180 * k for k in range(first, last + 1)]
    rows = []
    for angle in sorted(set(angles)):
        theta = math.radians(angle)
        bx, by = radius * math.cos(theta), radius * math.sin(theta)
        dx, dy = ax - bx, ay - by
        length = math.hypot(dx, dy)
        lever = (bx * dy - by * dx) / length if length > 1e-12 else 0.0
        singular = length <= 1e-12 or abs(lever) <= 1e-12
        force = None if singular else -moment / lever
        rows.append({"angle_deg": angle, "length_m": length, "signed_moment_arm_m": lever,
                     "signed_actuator_force_N": force,
                     "required_capacity_N": None if force is None else sf * abs(force),
                     "singular": singular})
    singular = any(r["singular"] for r in rows)
    required = None if singular else max(r["required_capacity_N"] for r in rows)
    lengths = [r["length_m"] for r in rows]
    stroke = max(lengths) - min(lengths)
    return {"model": "actuator", "positions": rows, "singular": singular,
            "min_length_m": min(lengths), "max_length_m": max(lengths), "stroke_m": stroke,
            "required_capacity_N": required, "force_capacity_N": capacity,
            "available_stroke_m": travel,
            "passes": not singular and required <= capacity and stroke <= travel}


def optimize_bracket(c):
    """Enumerate a discrete rectangular-beam design space; no global-optimum claim."""
    if not c["materials"] or not c["widths_m"] or not c["heights_m"]:
        raise ValueError("Provide materials, widths_m, and heights_m")
    mass_limit = get(c, "max_mass_kg", True)
    rows = []
    for m in c["materials"]:
        for width in c["widths_m"]:
            for height in c["heights_m"]:
                case = dict(c, material=m, width_m=width, height_m=height)
                result = cantilever(case)
                rows.append({"material": m["name"], "width_m": width, "height_m": height,
                             "mass_kg": result["mass_kg"],
                             "stress_Pa": result["root_bending_stress_Pa"],
                             "deflection_m": abs(result["tip_deflection_m"]),
                             "strength_utilization": result["checks"]["bending_Pa"]["utilization"],
                             "deflection_utilization": result["checks"]["tip_deflection_m"]["utilization"],
                             "mass_utilization": result["mass_kg"] / mass_limit,
                             "model_screen_passes": result["model_screen_passes"],
                             "passes": result["passes"] and result["mass_kg"] <= mass_limit})
    rows.sort(key=lambda r: (r["mass_kg"], r["material"], r["width_m"], r["height_m"]))
    feasible = [r for r in rows if r["passes"]]
    return {"model": "optimize_bracket", "candidate_count": len(rows),
            "feasible_count": len(feasible), "best": feasible[0] if feasible else None,
            "passes": bool(feasible), "candidates": rows}


MODELS = {"cantilever": cantilever, "shaft": shaft, "bolt_group": bolt_group,
          "actuator": actuator, "optimize_bracket": optimize_bracket}
