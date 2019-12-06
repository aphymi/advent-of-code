import inspect
from typing import Iterable, List, Sequence, Tuple, Union

# Type aliases
IntcodeProgram = List[int]
WriteAddrReturn = Tuple[int, int]
OutReturn = None
JumpReturn = int
OpFuncReturn = Union[WriteAddrReturn, OutReturn, JumpReturn]

def process_step(program: IntcodeProgram, pc: int):
	
	op = program[pc]

def get_args(
		program: IntcodeProgram,
		opcode: int,
		args: Sequence[int]
		) -> List[int]:
	
	pass

# A set of opcodes for which the last parameter should always be treated as an
# 	immediate
last_param_immediate = set(range(1, 9)).difference({4, 5, 6})

# A set of opcodes for which the pc should not be automatically incremented
# 	after their execution
no_pc_increment = {5, 6}

class IntcodeExecutor:
	program: IntcodeProgram
	inputs: Iterable[int]
	pc: int
	
	def __init__(
			self,
			program: IntcodeProgram, 
			inputs: Iterable[int],
			) -> None:
		self.program = program
		self.inputs = inputs
		self.pc = 0
	
	def step(self):
		cur_op = self.program[self.pc]
		
		opcode = cur_op % 100
		arg_modes = [
			int(mode)
			for mode in reversed(str(cur_op // 100))
		]
	
	def get_op_args(
			self,
			opcode: int,
			arg_modes: int
			) -> List[int]:
			
		op_arity = inspect.getargspec()
	
	def get_opcode_func(self, opcode: int) -> Callable[..., OpFuncReturn]:
		return getattr(self, f"op{opcode}")
