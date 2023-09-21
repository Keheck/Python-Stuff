import pygame.examples.aliens as aliens
import argparse
import sys

"""parser = argparse.ArgumentParser("Turnbased Strategy Game")
parser.add_argument("--width", default=720, type=int)
parser.add_argument("--height", default=405, type=int)
parser.add_argument("difficulty", choices=["easy", "medium", "hard"], default="easy", nargs="?")
parser.add_argument("map", default="?", nargs="?")

args = parser.parse_args()
print(args)

pygame.init()
screen = pygame.display.set_mode((args.width, args.height), pygame.OPENGL)

color = 0"""

aliens.main()