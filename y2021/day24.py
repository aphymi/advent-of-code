import operator
from pprint import pprint
from typing import Callable, Union

from util.printing import print_over_current
from util.utils import chunk


VariableName = str
Parameter = Union[VariableName, int]
BinaryOperation = Callable[[int, int], int]
InstructionFunction = Callable[[dict[str, int], list[int]], None]
InstructionParams = tuple[int, int, int]

def is_int(possible_num: str) -> bool:
	try:
		int(possible_num)
	except ValueError:
		return False
	else:
		return True


class OffbrandIntcode:
	"""
	A solver for general instruction sets isn't actually required for today's
	problem, so the majority of this class' functionality isn't used.

	I wrote it before I knew that that was the case, so I'm keeping it here
	anyway, for the sake of 'I like it'.
	"""
	instructions: list[str]

	vars = {
		"w": 0,
		"x": 0,
		"y": 0,
		"z": 0,
	}

	_processed_instructions: InstructionFunction

	def __init__(self, instructions: list[str]) -> None:
		self.instructions = instructions

		instruction_functions = [
			self.get_instruction_function(instruction)
			for instruction in instructions
		]

		def processed_instructions(vars, input_stack):
			for func in instruction_functions:
				func(vars, input_stack)

		self._processed_instructions = processed_instructions

	def get_input(self) -> int:
		return self.input_stack.pop()

	def do_bin_op(
		self,
		op: BinaryOperation,
		p1: VariableName,
		p2: Parameter,
	) -> None:
		p1_value = self.vars[p1]
		p2_value = self.vars[p2] if isinstance(p2, str) else p2

		self.vars[p1] = op(p1_value, p2_value)
	
	def get_instruction_function(
		self,
		instruction: str,
	) -> InstructionFunction:
		instruction_parts = instruction.split(" ")
		instruction_name = instruction_parts[0]
		parameters = instruction_parts[1:]

		(foo := 5)

		p1 = parameters[0]
		if instruction_name == "inp":
			def instruction(vars, input_stack):
				vars[p1] = input_stack.pop()
			
			return instruction

		else:
			p2 = (
				int(parameters[1]) if is_int(parameters[1]) else parameters[1]
			)

			ops = {
				"add": operator.add,
				"mul": operator.mul,
				"div": operator.floordiv,
				"mod": operator.mod,
				"eql": lambda a, b: 1 if a == b else 0,
			}

			op = ops[instruction_name]

			def instruction(vars, _input_stack):
				vars[p1] = op(vars[p1], p2 if isinstance(p2, int) else vars[p2])
			
			return instruction
	
	def do_instruction(
		self,
		instruction: str,
		input_stack: list[int],
	) -> None:
		instruction_parts = instruction.split(" ")
		instruction_name = instruction_parts[0]
		parameters = instruction_parts[1:]
		
		p1 = parameters[0]
		if instruction_name == "inp":
			self.vars[p1] = input_stack.pop()
		
		else:
			p2 = (
				int(parameters[1]) if is_int(parameters[1]) else parameters[1]
			)

			ops = {
				"add": operator.add,
				"mul": operator.mul,
				"div": operator.floordiv,
				"mod": operator.mod,
				"eql": lambda a, b: 1 if a == b else 0,
			}

			self.do_bin_op(ops[instruction_name], p1, p2)
	
	def print_state(self) -> None:
		print("\t".join(str(self.vars[c]) for c in "wxyz"))
	
	def run(self, input_queue: list[int]) -> None:
		input_stack = list(reversed(input_queue))
		# self.print_state()

		line = 1

		for instruction in self.instructions:
			self.do_instruction(instruction, input_stack)

			# print(f"{line}| ", end="")
			# self.print_state()
			line += 1
	
	def run_processed(self, input_queue: list[int]) -> None:
		"""
		Like run, but way faster.
		"""
		input_stack = list(reversed(input_queue))

		self._processed_instructions(self.vars, input_stack)
	
	def reset(self) -> None:
		self.vars = {
			"w": 0,
			"x": 0,
			"y": 0,
			"z": 0,
		}
	

class SpecialisedOI(OffbrandIntcode):
	instruction_params: list[tuple[int, int, int]]

	def __init__(self, instruction_params: list[InstructionParams]) -> None:
		self.instruction_params = instruction_params
	
	def run(self, input_queue: list[int]) -> None:
		input_stack = list(reversed(input_queue))

		for a, b, c in self.instruction_params:
			w = input_stack.pop()
			z = self.vars["z"]
			x = (z % 26) + b
			z //= a
			if x != w:
				z *= 26
				z += w + c
			
			self.vars["z"] = z

def extract_relevant_instruction_params(
	instructions: list[str],
) -> list[InstructionParams]:
	instruction_params = []
	for ic in chunk(instructions, 18):
		a = int(ic[4][6:])
		b = int(ic[5][6:])
		c = int(ic[15][6:])
		instruction_params.append((a, b, c))
	
	return instruction_params

def get_highest_compatible(
	i1: InstructionParams,
	i2: InstructionParams,
	decider_function: Callable[[int, int], int],
) -> str:
	program = SpecialisedOI([])
	program.instruction_params = [i1, i2]
	best_ij = None
	for i in range(1, 10):
		for j in range(1, 10):
			program.reset()
			program.run([i, j])
			if program.vars["z"] == 0:
				new_ij = int(str(i) + str(j))
				if best_ij is None:
					best_ij = new_ij
				else:
					best_ij = decider_function(best_ij, new_ij)

	if best_ij is None:
		raise Exception("Unable to find")
	
	return str(best_ij)

def solve_paired_params(
	instruction_params: list[tuple[int, int, int]],
	decider_function: Callable[[int, int], int],
) -> int:
	model_number_parts = [None] * len(instruction_params)
	stack = []
	for index, instruction_param in enumerate(instruction_params):
		if instruction_param[0] == 1:
			stack.append((index, instruction_param))
		else:
			prev_index, prev_params = stack.pop()
			model_part = get_highest_compatible(
				prev_params,
				instruction_param,
				decider_function,
			)
			model_number_parts[prev_index] = model_part[0]
			model_number_parts[index] = model_part[1]
		
	return int("".join(model_number_parts))

def part1(instructions: list[str]) -> int:
	# Today's problem is a reverse-engineering problem. As such, the intended
	# solution isn't to actually allow for arbitrary inputs, but to make certain
	# assumptions about the input and go from there. So, some assumptions:
	# 1. The given instruction set can be split into 14 near-identical
	# 	subprograms that are near-identical to a known template
	# 2. Each subprogram has three points of variability, those being the
	# 	second parameters on the following lines, given by index: 4, 5, -13
	# 3. A, B, and C fall under certain restrictions that allows subprograms to
	# 	be solved together as pairs
	# Each subprogram essentially boils down to:
	# w = <input> in [1, 9]
	# x = ((z % 26) + B)
	# z //= A
	# if x != w:
	# 	z *= 26
	# 	z += w + C
	instruction_params = extract_relevant_instruction_params(instructions)
	return solve_paired_params(instruction_params, max)

def part2(instructions: list[str]) -> int:
	instruction_params = extract_relevant_instruction_params(instructions)
	return solve_paired_params(instruction_params, min)
