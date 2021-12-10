import statistics

from util.parse import *


pairs = {
	"(": ")",
	"[": "]",
	"{": "}",
	"<": ">",
}

openers = pairs.keys()

def part1(lines: list[str]) -> int:
	syntax_error_score_map = {
		")": 3,
		"]": 57,
		"}": 1197,
		">": 25137,
	}

	total_score = 0

	for line in lines:
		evaluation_stack = []
		for char in line:
			if char in openers:
				evaluation_stack.append(char)
				continue

			char_is_error = (
				len(evaluation_stack) == 0
				or char != pairs[evaluation_stack[-1]]
			)

			if char_is_error:
				total_score += syntax_error_score_map[char]
				break

			evaluation_stack.pop()
	
	return total_score

def part2(lines: list[str]) -> int:
	score_map = {
		")": 1,
		"]": 2,
		"}": 3,
		">": 4,
	}

	scores = []
	for line in lines:
		evaluation_stack = []
		for char in line:
			if char in openers:
				evaluation_stack.append(char)
				continue

			char_is_error = (
				len(evaluation_stack) == 0
				or char != pairs[evaluation_stack[-1]]
			)

			if char_is_error:
				break

			evaluation_stack.pop()
		
		else:
			if not evaluation_stack:
				continue

			score = 0
			for char in reversed(evaluation_stack):
				score *= 5
				score += score_map[pairs[char]]
			
			scores.append(score)
	
	return statistics.median(scores)
