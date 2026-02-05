import json
import math
import argparse

G0 = 9.80665

def load_thrusters(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        return []

def calculate_fuel_mass(dry_mass, delta_v, isp):
    if isp <= 0: return float('inf')
    return dry_mass * (math.exp(delta_v / (isp * G0)) - 1)

def filter_and_rank(thrusters, required_dv, max_power, dry_mass):
    feasible = []
    
    for t in thrusters:
        if t['power_W'] > max_power:
            continue
        
        fuel_needed = calculate_fuel_mass(dry_mass, required_dv, t['isp_s'])
        thruster_hardware_mass = t['mass_kg']
        total_mass = dry_mass + thruster_hardware_mass + fuel_needed

        feasible.append({
            'name': t['name'],
            'type': t['type'],
            'power_W': t['power_W'],
            'thruster_mass': thruster_hardware_mass,
            'fuel_kg': round(fuel_needed, 3),
            'total_mass_kg': round(total_mass, 2)
        })

    return sorted(feasible, key=lambda x: x['total_mass_kg'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Thruster Selection Tool")
    parser.add_argument("--dv", type=float, required=True, help="Delta-V (m/s)")
    parser.add_argument("--power", type=float, required=True, help="Max Power (W)")
    parser.add_argument("--mass", type=float, required=True, help="Dry Mass (kg)")
    args = parser.parse_args()

    data = load_thrusters("thrusters.json")
    results = filter_and_rank(data, args.dv, args.power, args.mass)

    print(f"\n--- MISSION ANALYSIS ---")
    print(f"Target Delta-V: {args.dv} m/s | Satellite Dry Mass: {args.mass} kg | Power Limit: {args.power} W\n")

    if not results:
        print("No feasible thrusters found for these constraints.")
    else:
        print("Detailed Mass Calculations:")
        for r in results:
            print(f"- The {r['name']} needs {r['fuel_kg']} kg of fuel.")
            print(f"  Calculation: {args.mass} kg (Sat) + {r['thruster_mass']} kg (Thruster) + {r['fuel_kg']} kg (Fuel) = {r['total_mass_kg']} kg")
        
        print(f"\n--- RANKED RECOMMENDATIONS ---")
        print(f"{'NAME':<30} | {'TYPE':<15} | {'POWER(W)':<10} | {'TOTAL MASS(kg)'}")
        print("-" * 80)
        for r in results:
            print(f"{r['name']:<30} | {r['type']:<15} | {r['power_W']:<10} | {r['total_mass_kg']}")
