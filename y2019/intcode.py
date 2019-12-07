import collections
import inspect
from typing import Callable, Deque, Iterable, List, Tuple, Union

# Type aliases
IntcodeProgram = List[int]
WriteAddrReturn = Tuple[int, int]
OutReturn = None
JumpReturn = int
OpFuncReturn = Union[WriteAddrReturn, OutReturn, JumpReturn]

# A set of opcodes for which the last parameter should always be treated as an
# 	immediate
last_param_immediate = set(range(1, 9)).difference({4, 5, 6})

def run_program_to_completion(
		program: IntcodeProgram,
		inputs: Iterable[int] = None,
		) -> List[int]:
	"""
	Run an intcode program in-place to completion, returning the execution's
	outputs.
	"""
	
	executor = IntcodeExecutor(program, inputs)
	executor.run_to_completion()
	return executor.outputs

class IntcodeExecutor:
	program: IntcodeProgram
	inputs: Deque[int]
	pc: int
	
	outputs: List[int]
	
	def __init__(
			self,
			program: IntcodeProgram, 
			inputs: Iterable[int] = None,
			) -> None:
		self.program = program
		self.inputs = collections.deque(inputs or [])
		self.pc = 0
		
		self.outputs = []
	
	def run_to_completion(self) -> None:
		"""
		Run the intcode program until it hits an opcode of 99.
		"""
		
		# TODO Exception-based intcode program finishing.
		while self.program[self.pc] != 99:
			self.step()
	
	def step(self) -> None:
		"""
		Execute a single instruction of the intcode program.
		
		Returns: the output of the executed instruction, if any.
		"""
		
		cur_op = self.program[self.pc]
		
		opcode = cur_op % 100
		arg_modes = [
			int(mode)
			for mode in reversed(str(cur_op // 100))
		]
		args = self.get_op_args(opcode, arg_modes)
		
		op_func = self.get_opcode_func(opcode)
		op_arity = self.get_opcode_arity(opcode)
		
		# Increment the pc prior to running the function, so that jump ops may
		# 	modify it if necessary.
		self.pc += op_arity + 1
		
		op_return_val = op_func(*args)
		if op_return_val is not None:
			self.outputs.append(op_return_val)
		
	
	def get_op_args(
			self,
			opcode: int,
			arg_modes: int
			) -> List[int]:
			
		op_arity = self.get_opcode_arity(opcode)
		processed_args = []
		
		raw_args = self.program[self.pc + 1: self.pc + op_arity + 1]
		
		for index, raw_arg in enumerate(raw_args):
			arg_mode: int
			if index == (op_arity - 1) and opcode in last_param_immediate:
				arg_mode = 1
			elif index >= len(arg_modes):
				arg_mode = 0
			else:
				arg_mode = arg_modes[index]
			
			if arg_mode == 0:
				processed_args.append(self.program[raw_arg])
			
			elif arg_mode == 1:
				processed_args.append(raw_arg)
			
			else:
				raise Exception(
					f"Unknown argument mode in intcode program: {arg_mode}"
				)
		
		return processed_args
	
	
	def get_opcode_func(self, opcode: int) -> Callable[..., OpFuncReturn]:
		return getattr(self, f"op{opcode}")
	
	def get_opcode_arity(self, opcode: int) -> int:
		# Get the full number of args, then subtract one to account for 'self'.
		return len(
			inspect.getfullargspec(self.get_opcode_func(opcode)).args
		) - 1
	
	def op1(self, arg1: int, arg2: int, write_addr: int) -> None:
		"""
		Add two numbers together.
		"""
		
		self.program[write_addr] = arg1 + arg2

	def op2(self, arg1: int, arg2: int, write_addr: int) -> None:
		"""
		Multiply two numbers together.
		"""
		
		self.program[write_addr] = arg1 * arg2
	
	def op3(self, write_addr: int) -> None:
		"""
		Pop an input from the input list and write it to the specified addr.
		"""
		
		if len(self.inputs) == 0:
			raise Exception("Attempted intcode input, but input list is empty.")
		
		self.program[write_addr] = self.inputs.popleft()
	
	def op4(self, arg: int) -> int:
		"""
		Return the given value. Equivalent to an echo.
		"""
		
		return arg
	
	def op5(self, do_jump: int, new_pc: int) -> None:
		"""
		Set the pc to the given value if do_jump is nonzero.
		"""
		
		if do_jump != 0:
			self.pc = new_pc
	
	def op6(self, do_not_jump: int, new_pc: int) -> None:
		"""
		Set the pc to the given value if do_not_jump is nonzero.
		"""
		
		if do_not_jump == 0:
			self.pc = new_pc
		
	def op7(self, arg1: int, arg2: int, write_addr: int) -> None:
		"""
		Set the given address to 1 if arg1 is less than arg2, or 0 otherwise.
		"""
		
		self.program[write_addr] = int(arg1 < arg2)
	
	def op8(self, arg1: int, arg2: int, write_addr: int) -> None:
		"""
		Set the given address to 1 if arg1 is equal to arg2, or 0 otherwise.
		"""
		
		self.program[write_addr] = int(arg1 == arg2)
