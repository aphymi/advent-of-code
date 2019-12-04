from typing import List

IntcodeProgram = List[int]

def run_program_to_completion(prog: IntcodeProgram) -> None:
	"""
	Run an intcode program to completion.
	"""
	
	pc = 0
	
	while True:
		opcode = prog[pc]
		
		if opcode == 99:
			break
			
		elif opcode == 1:
			prog[prog[pc+3]] = prog[prog[pc+1]] + prog[prog[pc+2]]
			pc += 4
		
		elif opcode == 2:
			prog[prog[pc+3]] = prog[prog[pc+1]] * prog[prog[pc+2]]
			pc += 4
		
		else:
			raise Exception(
				f"Unknown opcode '{opcode}' in Intcode program "
				"execution"
			)
