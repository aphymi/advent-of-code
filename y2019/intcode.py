import inspect
from typing import Callable, Dict, List, Tuple, Union

IntcodeProgram = List[int]

opcodes: Dict[int, Callable[..., Union[Tuple[int, int], None]]] = {
	1: lambda arg1, arg2, out_addr: (out_addr, arg1+arg2),
	
	2: lambda arg1, arg2, out_addr: (out_addr, arg1*arg2),
	
	3: lambda write_addr: (write_addr, int(input("In: "))),
	
	4: lambda arg1: print(f"Out: {arg1}"),
	
	5: lambda jump, new_pc: new_pc if jump else None,
	
	6: lambda no_jump, new_pc: None if no_jump else new_pc,
	
	7: lambda arg1, arg2, write_addr: (write_addr, int(arg1 < arg2)),
	
	8: lambda arg1, arg2, write_addr: (write_addr, int(arg1 == arg2)),
}

# A list of opcodes for whom the last parameter is a write address, and so
# 	should be treated as an immediate for the purpose of value-finding,
# 	regardless of specified mode.
last_param_immediate = set(range(1, 9)).difference({4, 5, 6})

# Opcodes whose first return value is a new pc, rather than a write address.
jumps = set((
	5,
	6,
))

def run_program_to_completion(prog: IntcodeProgram) -> None:
	"""
	Run an intcode program to completion.
	"""
	
	pc = 0
	
	while True:
		op = prog[pc]
		opcode = op % 100
		
		if opcode == 99:
			break
		
		arg_modes = [
			int(mode)
			for mode in reversed(str(op // 100))
		]
		
		op_func = opcodes[opcode]
		op_arity = len(inspect.getargspec(op_func).args)
		
		# Pad the arg_mode list until it's length is the same as the op arity.
		arg_modes += [0] * (op_arity - len(arg_modes))
		
		if opcode in last_param_immediate:
			# Set the last mode to immediate.
			arg_modes[-1] = 1
		
		args = []
		for arg, mode in zip(prog[pc+1:pc+op_arity+1], arg_modes):
			arg_value: int
			if mode == 0: # Position mode
				arg_value = prog[arg]
				
			elif mode == 1: # Immediate mode
				arg_value = arg
			
			else:
				raise Exception(f"Unknown argument mode: {mode}")
			
			args.append(arg_value)
		
		returned = op_func(*args)
		if returned is None:
			# Just printed something out.
			pc += op_arity + 1
		
		elif opcode in jumps:
			pc = returned
		
		else:
			# Write the second value of the tuple at the first value.
			prog[returned[0]] = returned[1]
			pc += op_arity + 1
