from argparse import ArgumentParser, FileType

parser = ArgumentParser("Read and write .wav files idk\n")
parser.add_argument("-in", type=FileType("rb"))
parser.add_argument("-out", type=FileType("w+b"), default=r".\output.wav")
parser.add_argument("-fourier-slice", type=float, default=0.001)

pitch_group = parser.add_mutually_exclusive_group()
pitch_group.add_argument("-pitch-shift", type=float, default=0)
pitch_group.add_argument("-pitch-factor", type=float, default=1)

arguments = parser.parse_args()
