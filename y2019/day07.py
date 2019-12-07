import itertools
from typing import List

from util.parse import *
from y2019 import intcode

parse_input = compose(get_ints, single_line)


def feed_input_through_amplifiers(
		program: intcode.IntcodeProgram,
		phases: List[int],
		) -> int:
	
	last_output = 0
	for phase in phases:
		program_copy = program.copy()
		outputs = intcode.run_program_to_completion(
			program_copy,
			inputs=[phase, last_output],
		)
		last_output = outputs[0]
	
	return last_output

def run_through_feedback_mode(
		program: intcode.IntcodeProgram,
		phases: List[int],
		) -> int:
	
	executors = [
		intcode.IntcodeExecutor(program.copy(), [phase])
		for phase in phases
	]
	
	last_exec_ind = -1
	last_outputs = [0]
	done = False
	while executors[-1].program[executors[-1].pc] != 99:
		cur_executor_ind = (last_exec_ind + 1) % len(executors)
		cur_executor = executors[cur_executor_ind]
		
		cur_executor.inputs.extend(last_outputs)
		# Run the current executor until it's about to run an input command on
		# 	an empty input.
		while not (
				(cur_executor.program[cur_executor.pc] % 100) == 3 and
				len(cur_executor.inputs) == 0):
			try:
				cur_executor.step()
			except AttributeError:
				# Reached opcode 99
				break
		
		last_outputs = cur_executor.outputs
		cur_executor.outputs = []
		
		last_exec_ind = cur_executor_ind
		if done:
			break
	
	return last_outputs[-1]
		

def get_possible_phase_settings(length: int = 5) -> List[int]:
	for perm in itertools.permutations([0,1,2,3,4]):
		yield perm
	
	"""
	if length == 0:
		yield []
	
	else:
		for phase in range(0, 5):
			for setting in get_possible_phase_settings(length - 1):
				yield [phase] + setting
	"""
	

def part1(program: intcode.IntcodeProgram) -> int:
	program = program[:]
	
	return max((
		feed_input_through_amplifiers(program, phases)
		for phases in itertools.permutations(range(0, 5))
	))

def part2(program: intcode.IntcodeProgram) -> int:
	program = program[:]
	
	return max((
		run_through_feedback_mode(program, phases)
		for phases in itertools.permutations(range(5, 10))
	))
