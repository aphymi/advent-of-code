from util.parse import *
from y2019 import intcode

parse_input = compose(single_line, get_ints)

def part1(program: intcode.IntcodeProgram) -> int:
	intcode.run_program_to_completion(program)

part2 = part1
