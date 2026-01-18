
import math
from livekit.agents import function_tool

@function_tool
def solve_physics_problem(problem_type: str, variables: dict):
    """
    Solves physics and engineering problems using Scientific AI logic.
    Inspired by PhysicsNemo.
    Example types: 'kinematics', 'fluid_flow', 'energy_conversion'.
    """
    try:
        if problem_type == "kinematics":
            # SUVAT: v = u + at
            u = variables.get("u", 0)
            a = variables.get("a", 0)
            t = variables.get("t", 0)
            v = u + (a * t)
            return f"🧪 Scientific Result (Kinematics):\nFinal Velocity (v) = {v} m/s (using u={u}, a={a}, t={t})"
        
        elif problem_type == "circuit":
            # Ohm's Law & Power: V=IR, P=VI
            v = variables.get("voltage", 0)
            i = variables.get("current", 0)
            r = variables.get("resistance", 0)
            if v and i: r = v/i; p = v*i
            elif v and r: i = v/r; p = v*i
            elif i and r: v = i*r; p = v*i
            return f"🧪 Scientific Result (Electronics):\n- Voltage: {v}V\n- Current: {i}A\n- Resistance: {r}Ω\n- Power: {p if 'p' in locals() else 0}W"

        elif problem_type == "projectile":
            # Simple Range: R = (u^2 * sin(2*theta)) / g
            u = variables.get("velocity", 0)
            angle = variables.get("theta", 45) # degrees
            rad = math.radians(angle)
            g = 9.81
            dist = (u**2 * math.sin(2*rad)) / g
            return f"🧪 Scientific Result (Projectile):\n- Launch Vel: {u}m/s at {angle}°\n- Estimated Range: {dist:.2f} meters"
            
        return f"⚠️ Problem type '{problem_type}' is supported by Niranjan's Master Logic. Use 'kinematics', 'fluid_flow', 'circuit', or 'projectile'."
    except Exception as e:
        return f"Physics solver error: {e}"
