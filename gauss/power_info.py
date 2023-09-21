from math import pi
import math

# Constants
vacuum_permeability = 4*pi*10**-7
specific_resistance = 0.0089
magnetic_suceptibility = 200_000
density = 7_874

# Projectile
volume = 0.00391**2 * pi * 0.05

# Coil
voltage = 200
wire_cross_section = 0.5**2 * pi
coil_turns = 200
coil_length = 0.2
coil_radius = 0.1
additional_wire = 0.2

# Additional calculations
coil_circumference = 2 * coil_radius * pi
coil_wire_length = math.sqrt((coil_length / coil_turns) ** 2 + coil_circumference ** 2) * coil_turns + additional_wire
coil_resistance = specific_resistance * coil_wire_length / wire_cross_section

def vexit():
    coil_turns_per_length = coil_turns / coil_length
    current = voltage / coil_resistance
    return math.sqrt(2 / density * vacuum_permeability * magnetic_suceptibility * coil_turns_per_length ** 2 * current ** 2)

print(f"Inductivity: {1000*coil_turns**2 * 1 * vacuum_permeability * (coil_radius ** 2 * pi)/coil_length:.2f}mH")
print(f"Resistance: {coil_resistance:.4f}Ω")
print(f"Current: {voltage / coil_resistance:.4f}A")
print(f"Exit Velocity: {vexit():.2f}m/s")
print(f"Mass: {(density * volume)*1000:0.2f}g")
print(f"Muzzle Energy: {(vexit() ** 2 * (density*volume) * 0.5):0.4f}J")
