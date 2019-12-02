from util.parse import *

parse_input = compose(single_line, get_ints)

def run_intcode_program(program):
	program = program[:] # Make a copy
	pc = 0
	
	while program[pc] != 99:
		opcode = program[pc]
		if opcode == 1:
			program[program[pc+3]] = program[program[pc+1]] + program[program[pc+2]]
		
		elif opcode == 2:
			program[program[pc+3]] = program[program[pc+1]] * program[program[pc+2]]
			
		else:
			raise Exception("Unknown opcode in intcode program")
	
		pc += 4
	
	return program

def part1(program):
	program = program[:] # Make a copy.
	program[1] = 12
	program[2] = 2
	
	program = run_intcode_program(program)
	
	return program[0]

def part2(program):
	
	for i in range(0, 100):
		for j in range(0, 100):
			new_program = program[:] # Make a copy.
			
			new_program[1] = i
			new_program[2] = j
			
			new_program = run_intcode_program(new_program)
			
			if new_program[0] == 19690720:
				return (100 * i) + j
	
	raise Exception("No valid noun and verb found")
