from math import sqrt
import si_unit

capacitance = 680e-6
inductance = 7.9e-3

print(f"Resistance: {sqrt(4 * inductance / capacitance):0.2f}Ω")