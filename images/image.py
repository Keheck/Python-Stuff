from ast import parse
from PIL import Image
from argparse import ArgumentParser, FileType
import pygame
import pathlib

parser = ArgumentParser()
parser.add_argument("name", type=str)
parser.add_argument("-right-padding", type=int, default=20)
parser.add_argument("-left-padding", type=int, default=20)
parser.add_argument("-corner-shape", choices=["sharp", "round"])
parser.add_argument("-round-radius", type=float, default=0.1)
parser.add_argument("output", type=pathlib.Path)

args = parser.parse_args()

pygame.font.init()
font = pygame.font.Font(None, 24)
name = font.render(args.name, False, (0, 0, 0))
