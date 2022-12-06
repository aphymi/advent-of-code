import string

from util.parse import *
from util.utils import chunk


parse_input = map_func(
	lambda line: (line[:len(line)//2], line[len(line)//2:]),
)

Rucksack = tuple[str, str]

def get_priority(item_type: str) -> int:
	if item_type in string.ascii_lowercase:
		return string.ascii_lowercase.index(item_type) + 1
	
	return string.ascii_uppercase.index(item_type) + 27

def get_misplaced_item_type(rucksack: Rucksack) -> str:
	return set(rucksack[0]).intersection(rucksack[1]).pop()

def get_badge_type(rucksack_group: list[Rucksack]) -> str:
	a, b, c = rucksack_group
	common_types = (
		set("".join(a)).intersection("".join(b)).intersection("".join(c))
	)
	return common_types.pop()

def part1(rucksacks: list[Rucksack]) -> int:
	return sum(
		get_priority(get_misplaced_item_type(rucksack))
		for rucksack in rucksacks
	)

def part2(rucksacks: list[Rucksack]) -> int:
	return sum(
		get_priority(get_badge_type(rucksack_group))
		for rucksack_group in chunk(rucksacks, 3)
	)
