import copy
import itertools

from util.parse import *


parse_input = compose(
	joined_line,
	lambda inp: inp.split("\n\n"),
	zip_input_with(
		lambda stack_drawing: list(zip(
			*(
				line[1::4]
				for line in stack_drawing.split("\n")
			)
		)),
		lambda instructions: instructions.split("\n"),
	),
	zip_input_with(
		lambda stacks: {
			int(stack[-1]): list(reversed(list(itertools.dropwhile(
				lambda crate: crate == " ",
				stack[:-1],
			))))
			for stack in stacks
		},
		get_ints,
	),
)

CrateStack = list[int]
CrateStacks = dict[int, CrateStack]

CrateMoveInstruction = tuple[int, int, int]

def apply_instruction(
	crate_stacks: CrateStacks,
	instruction: CrateMoveInstruction,
	can_pick_up_multiple_crates: bool = False
) -> None:
	num_to_move, from_stack_num, to_stack_num = instruction
	from_stack = crate_stacks[from_stack_num]
	to_stack = crate_stacks[to_stack_num]

	crates_to_move = from_stack[-num_to_move:]
	crate_stacks[from_stack_num] = from_stack[:-num_to_move]

	if not can_pick_up_multiple_crates:
		crates_to_move.reverse()

	to_stack.extend(crates_to_move)

def part1(inp: tuple[CrateStacks, list[CrateMoveInstruction]]) -> str:
	crate_stacks, instructions = inp
	crate_stacks = copy.deepcopy(crate_stacks)

	for instruction in instructions:
		apply_instruction(crate_stacks, instruction)

	return "".join(stack[-1] for stack in crate_stacks.values())

def part2(inp: tuple[CrateStacks, list[CrateMoveInstruction]]) -> str:
	crate_stacks, instructions = inp
	crate_stacks = copy.deepcopy(crate_stacks)

	for instruction in instructions:
		apply_instruction(crate_stacks, instruction, True)

	return "".join(stack[-1] for stack in crate_stacks.values())
