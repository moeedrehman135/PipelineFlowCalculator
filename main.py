import math

def calculate_reynolds_number(density, velocity, diameter, viscosity):
    """Calculate the Reynolds number."""
    return (density * velocity * diameter) / viscosity

def calculate_friction_factor(reynolds_number, roughness, diameter):
    """Calculate the friction factor using the Colebrook-White equation."""
    if reynolds_number < 2300:  # Laminar flow
        return 64 / reynolds_number
    else:  # Turbulent flow, iterative approach for Colebrook equation
        def colebrook(f):
            return -2 * math.log10((roughness / (3.7 * diameter)) + (2.51 / (reynolds_number * math.sqrt(f)))) - 1 / math.sqrt(f)

        # Initial guess for friction factor
        f_guess = 0.02
        for _ in range(100):  # Iterative calculation
            f_guess = 1 / (colebrook(f_guess)**2)
        return f_guess

def calculate_pressure_drop(length, diameter, density, velocity, friction_factor):
    """Calculate pressure drop using the Darcy-Weisbach equation."""
    return friction_factor * (length / diameter) * (density * velocity**2 / 2)

def calculate_velocity(flow_rate, diameter):
    """Calculate velocity from flow rate."""
    area = math.pi * (diameter / 2)**2
    return flow_rate / area

def main():
    print("Pipeline Flow Calculator")
    print("1. Calculate Pressure Drop")
    print("2. Calculate Flow Rate")
    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        # Inputs for pressure drop calculation
        length = float(input("Enter the pipe length (m): "))
        diameter = float(input("Enter the pipe diameter (m): "))
        roughness = float(input("Enter the pipe roughness (m): "))
        density = float(input("Enter the fluid density (kg/m³): "))
        viscosity = float(input("Enter the fluid viscosity (Pa·s): "))
        velocity = float(input("Enter the fluid velocity (m/s): "))

        reynolds_number = calculate_reynolds_number(density, velocity, diameter, viscosity)
        friction_factor = calculate_friction_factor(reynolds_number, roughness, diameter)
        pressure_drop = calculate_pressure_drop(length, diameter, density, velocity, friction_factor)

        print(f"\nResults:")
        print(f"Reynolds Number: {reynolds_number:.2f}")
        print(f"Friction Factor: {friction_factor:.4f}")
        print(f"Pressure Drop: {pressure_drop:.2f} Pa")

    elif choice == 2:
        # Inputs for flow rate calculation
        length = float(input("Enter the pipe length (m): "))
        diameter = float(input("Enter the pipe diameter (m): "))
        roughness = float(input("Enter the pipe roughness (m): "))
        density = float(input("Enter the fluid density (kg/m³): "))
        viscosity = float(input("Enter the fluid viscosity (Pa·s): "))
        pressure_drop = float(input("Enter the pressure drop (Pa): "))

        # Guessing velocity and iterating to solve for flow rate
        velocity = 1.0  # Initial guess for velocity
        for _ in range(100):  # Iterative calculation
            reynolds_number = calculate_reynolds_number(density, velocity, diameter, viscosity)
            friction_factor = calculate_friction_factor(reynolds_number, roughness, diameter)
            calc_pressure_drop = calculate_pressure_drop(length, diameter, density, velocity, friction_factor)
            velocity = velocity * (pressure_drop / calc_pressure_drop)**0.5

        flow_rate = velocity * math.pi * (diameter / 2)**2

        print(f"\nResults:")
        print(f"Reynolds Number: {reynolds_number:.2f}")
        print(f"Friction Factor: {friction_factor:.4f}")
        print(f"Flow Rate: {flow_rate:.4f} m³/s")

    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
