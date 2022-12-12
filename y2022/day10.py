from util.parse import *
from util.utils import chunk


class VideoSystem:
	x = 1
	cycles = 0
	video_output = []

	def __init__(self) -> None:
		self.video_output = []

	def get_draw_position(self) -> int:
		return (self.cycles - 1) % 40
	
	def draw_current(self) -> None:
		draw_position = self.get_draw_position()

		draw = (self.x - 1) <= draw_position <= (self.x + 1)

		self.video_output.append("#" if draw else ".")
	
	def run_instruction(self, instruction: str) -> None:
		instruction_parts = instruction.split(" ")

		if instruction_parts[0] == "noop":
			self.cycles += 1
			self.draw_current()
		
		elif instruction_parts[0] == "addx":
			self.cycles += 1
			self.draw_current()
			self.cycles += 1
			self.draw_current()
			self.x += int(instruction_parts[1])
		
		else:
			raise Exception(f"Unknown instruction: {instruction}")
	
	def run_instructions(
		self,
		instructions: list[str],
		relevant_cycles: list[int] = [],
	) -> list[int]:
		relevant_cycles_stack = list(reversed(sorted(relevant_cycles)))
		relevant_signal_strengths = []

		last_x = self.x
		latest_relevant_cycle = (
			relevant_cycles_stack.pop()
			if relevant_cycles_stack
			else float("inf")
		)
		for instruction in instructions:
			self.run_instruction(instruction)
			if self.cycles == latest_relevant_cycle:
				relevant_signal_strengths.append(
					last_x * self.cycles,
				)

				if not relevant_cycles_stack:
					latest_relevant_cycle = float("inf")
				else:
					latest_relevant_cycle = relevant_cycles_stack.pop()
			
			elif self.cycles > latest_relevant_cycle:
				# Passed the relevant cycle with the last instruction
				relevant_signal_strengths.append(
					last_x * latest_relevant_cycle,
				)

				if not relevant_cycles_stack:
					latest_relevant_cycle = float("inf")
				else:
					latest_relevant_cycle = relevant_cycles_stack.pop()
			
			last_x = self.x
		
		return relevant_signal_strengths
	
	def print_video_output(self) -> None:
		for row in chunk(self.video_output, 40):
			print("".join(row))

def part1(instructions: list[str]) -> int:
	relevant_strengths = VideoSystem().run_instructions(
		instructions,
		[20, 60, 100, 140, 180, 220]
	)
	return sum(relevant_strengths)

def part2(instructions: list[str]) -> int:
	vs = VideoSystem()
	vs.run_instructions(instructions)

	vs.print_video_output()
	return "see print output"
