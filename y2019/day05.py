from util.parse import *
from y2019 import intcode

parse_input = compose(get_ints, single_line)

def part1(program: intcode.IntcodeProgram) -> int:
	intcode.run_program_to_completion(program)

part2 = part1
