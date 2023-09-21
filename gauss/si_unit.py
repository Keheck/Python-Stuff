import typing
import sys


class UnitDimension:
    def __init__(self, time=0, length=0, mass=0, current=0, temperature=0, substance=0, luminosity=0, special_symbol=None):
        self.time = time
        self.length = length
        self.mass = mass
        self.current = current
        self.temperature = temperature
        self.substance = substance
        self.luminosity = luminosity
        self.special_symbol = special_symbol
        
    def __getitem__(self, key):
        return {
            "time": self.time,
            "length": self.length,
            "mass": self.mass,
            "current": self.current,
            "temperatur": self.temperature,
            "substance": self.substance,
            "luminosity": self.luminosity
        }[key]
    
    def __add__(self, other):
        return UnitDimension(self.time + other.time, self.length + other.length, self.mass + other.length, self.current + other.current, 
        self.temperature + other.temperature, self.substance + other.substance, self.luminosity + other.luminosity)
    
    def __sub__(self, other):
        return UnitDimension(self.time - other.time, self.length - other.length, self.mass - other.length, self.current - other.current, 
        self.temperature - other.temperature, self.substance - other.substance, self.luminosity - other.luminosity)
    
    def __eq__(self, other):
        return self.time == other.time and self.length == other.length and self.mass == other.mass and self.current == other.current and self.temperature == other.temperature and self.substance == other.substance and self.luminosity == other.luminosity

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        # if self.special_symbol:
        #     return self.special_symbol

        unit_list = [(self.time, "s"), (self.length, "m"), (self.mass, "kg"), (self.current, "A"), (self.temperature, "K"), (self.substance, "mol"), (self.luminosity, "cd")]
        numerator = list(filter(lambda x: x[0] > 0, unit_list))
        denominator = list(filter(lambda x: x[0] < 0, unit_list))

        return ("*".join(map(lambda tup: f"{tup[1]}^{tup[0]}" if tup[0] != 1 else tup[1], numerator)) or "1") + "/" + ("*".join(map(lambda tup: f"{tup[1]}^{tup[0]}" if tup[0] != -1 else tup[1], denominator)) or "1")
            




SCALAR = UnitDimension()
SECOND = UnitDimension(time=1)
METER = UnitDimension(length=1)
KILOGRAM = UnitDimension(mass=1)
AMPERE = UnitDimension(current=1)
KELVIN = UnitDimension(temperature=1)
MOL = UnitDimension(substance=1)
CANDELA = UnitDimension(luminosity=1)

FORCE = UnitDimension(-2, 1, 1, special_symbol="F")
ENERGY = UnitDimension(-2, 2, 1, special_symbol="E")
VOLTAGE = UnitDimension(-3, 2, 1, -1, special_symbol="V")
FREQUENCY = UnitDimension(-1, special_symbol="Hz")

print(FORCE)
print(ENERGY)
print(VOLTAGE)
print(FREQUENCY)


class Unit:
    def __init__(self, dimension: UnitDimension, value: float):
        self.dimension = dimension
        self.value = value

    @staticmethod
    def check_dimension(a, b):
        if a.dimension != b.dimension:
            raise ValueError(f"The operands for this operation did not have matching units, operand 1 was {a.dimension} but operand 2 was {b.dimension}")
        return

    def __add__(self, other):
        check_dimension(self, other)
        return Unit(self.dimension, self.value + other.value)
    
    def __sub__(self, other):
        check_dimension(self, other)
        return Unit(self.dimension, self.value - other.value)
    
    def __mul__(self, other):
        return Unit(self.dimension + other.dimension, self.value * other.value)
    
    def __truediv__(self, other):
        return Unit(self.dimension - other.dimension, self.value / other.value)

    def __eq__(self, other):
        check_dimension(self, other)
        return self.value == other.value

    def __ne__(self, other):
        check_dimension(self, other)
        return self.value != other.value
    
    def __lt__(self, other):
        check_dimension(self, other)
        return self.value < other.value
    
    def __gt__(self, other):
        check_dimension(self, other)
        return self.value > other.value

    def __le__(self, other):
        check_dimension(self, other)
        return self.value <= other.value

    def __ge__(self, other):
        check_dimension(self, other)
        return self.value >= other.value