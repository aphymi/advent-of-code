import collections
import copy
import dataclasses
import math
from typing import Callable

from util.parse import *


@dataclasses.dataclass
class MonkeyInfo:
	items: list[int]
	operation: str
	divisibility_test: int
	next_monkeys: tuple[int, int]

parse_input = compose(
	joined_line,
	lambda inp: inp.split("\n\n"),
	split_on("\n"),
	map_func(
		lambda monkey_info: MonkeyInfo(
			[int(item) for item in monkey_info[1][18:].split(", ")],
			monkey_info[2][19:],
			int(monkey_info[3][21:]),
			(
				int(monkey_info[4][29:]),
				int(monkey_info[5][30:]),
			),
		),
	),
)

def safe_eval(expression: str, old: int) -> int:
	parts = expression.split()

	a = old if parts[0] == "old" else int(parts[0])
	b = old if parts[2] == "old" else int(parts[2])
	if parts[1] == "+":
		return a + b

	elif parts[1] == "*":
		return a * b
	
	else:
		raise Exception(f"Unknown operation: {parts[1]}")

def simulate_monkeys(
	monkeys: list[MonkeyInfo],
	rounds: int,
	management_function: Callable[[int], int] = lambda x: x // 3,
) -> list[int]:
	monkeys = copy.deepcopy(monkeys)
	inspection_counts = collections.defaultdict(int)

	for _i in range(rounds):
		for monkey_number, monkey in enumerate(monkeys):
			for item_worry_level in monkey.items:
				inspection_counts[monkey_number] += 1
				
				new_level = safe_eval(
					monkey.operation,
					item_worry_level,
				)

				new_level = management_function(new_level)

				new_monkey_number = (
					monkey.next_monkeys[0]
					if new_level % monkey.divisibility_test == 0
					else monkey.next_monkeys[1]
				)

				monkeys[new_monkey_number].items.append(new_level)
			
			monkey.items = []
	
	return inspection_counts

def part1(monkeys: list[MonkeyInfo]) -> int:
	inspection_counts = simulate_monkeys(monkeys, 20)

	return math.prod(list(sorted(inspection_counts.values()))[-2:])

def part2(monkeys: list[MonkeyInfo]) -> int:
	divisibility_multiple = (
		math.prod(monkey.divisibility_test for monkey in monkeys)
	)

	inspection_counts = simulate_monkeys(
		monkeys,
		10000,
		lambda x: x % divisibility_multiple,
	)

	return math.prod(list(sorted(inspection_counts.values()))[-2:])
