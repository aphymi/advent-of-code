from __future__ import annotations
from copy import deepcopy
from typing import List, Set, Tuple

from util.parse import *
from util.utils import flatten


class BingoBoard:
	def __init__(
		self,
		board: List[List[int]],
		marked: Set[int] = set(),
		last_mark_called: int = None
	) -> None:
		self.board = board
		self.marked = marked
		self.last_mark_called = last_mark_called
	
	def mark(self, number: int) -> BingoBoard:
		return BingoBoard(self.board, self.marked.union({number}), number)
	
	def get_score(self) -> int:
		unmarked = [
			space
			for space in flatten(self.board)
			if space not in self.marked
		]

		return sum(unmarked) * self.last_mark_called

	def has_win(self) -> bool:
		return (
			self.has_horiz_win()
			or self.has_vert_win()
			# or self.has_diagonal_win()
		)
	
	def has_horiz_win(self) -> bool:
		return any(
			all(
				space in self.marked
				for space in row
			)
			for row in self.board
		)
	
	def has_vert_win(self) -> bool:
		return any(
			all(
				space in self.marked
				for space in column
			)
			for column in zip(*self.board)
		)
	
	def has_diagonal_win(self) -> bool:
		left_to_right = [
			self.board[i][i]
			for i in range(len(self.board[0]))
		]
		right_to_left = [
			self.board[i][-(i+1)]
			for i in range(len(self.board[0]))
		]

		return any(
			all(
				space in self.marked for space in spaces
			)
			for spaces in (left_to_right, right_to_left)
		)
	
	def print_state(self) -> None:
		for row in self.board:
			for space in row:
				if space in self.marked:
					print("XX", end=" ")
				else:
					if space < 10:
						print(f" {space}", end=" ")
					else:
						print(space, end=" ")
			print()

parse_input = compose(
	get_ints,
	lambda lines: (
		lines[0],

	)
)

InputType = Tuple[List[int], List[BingoBoard]]

def parse_input(lines: List[str]) -> InputType:
	intified_lines = get_ints(lines)

	marks = intified_lines[0]

	boards = []
	for board_start_row_index in range(2, len(lines), 6):
		boards.append(
			BingoBoard(
				intified_lines[board_start_row_index:board_start_row_index + 5]
			)
		)
	
	return (marks, boards)


def part1(day_input: InputType) -> int:
	called_numbers, boards = day_input

	winning_board = None
	for called_number in called_numbers:
		if winning_board:
			break

		boards = [
			board.mark(called_number)
			for board in boards
		]

		for board in boards:
			if board.has_win():
				winning_board = board
		
	return winning_board.get_score()

def part2(day_input: InputType) -> int:
	called_numbers, boards = day_input

	losing_board = None
	for called_number in called_numbers:
		boards = [
			board.mark(called_number)
			for board in boards
		]

		if len(boards) == 1 and boards[0].has_win():
			losing_board = boards[0]
			break
		
		boards = [board for board in boards if not board.has_win()]
	
	return losing_board.get_score()
