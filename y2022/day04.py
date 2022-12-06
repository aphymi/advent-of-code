from util.parse import *


parse_input = compose(
	get_pos_ints,
	map_func(lambda line: ((line[0], line[1]), (line[2], line[3]))),
)

Sections = tuple[int, int]
SectionsPair = tuple[Sections, Sections]

def fully_overlaps(assignment: SectionsPair) -> bool:
	for order in (assignment, list(reversed(assignment))):
		overlaps =  (
			order[0][0] <= order[1][0]
			and order[0][1] >= order[1][1]
		)
		if overlaps:
			return True
		
	return False

def overlaps_at_all(assignment: SectionsPair) -> bool:
	sorted_assignment = list(sorted(assignment))

	return not sorted_assignment[0][1] < sorted_assignment[1][0]

def part1(assignments: list[SectionsPair]) -> int:
	return sum(
		1
		for assignment in assignments
		if fully_overlaps(assignment)
	)

def part2(assignments: list[SectionsPair]) -> int:
	return sum(
		1
		for assignment in assignments
		if overlaps_at_all(assignment)
	)
