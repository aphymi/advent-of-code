import functools
import itertools

from util.parse import *
from util.utils import chunk


# def save_list_eval(list_string: str) -> list:
# 	list_stack = []
# 	latest_list = None
# 	latest_number = ""
# 	for c in list_string:
# 		if c == "[":

parse_input = compose(
	lambda lines: [line for line in lines if line],
	map_func(eval),
)

Signal = list
SignalPair = tuple[Signal, Signal]

def cmp_signals(s1: Signal, s2: Signal) -> int:
	if isinstance(s1, list) and isinstance(s2, int):
		return cmp_signals(s1, [s2])
	
	if isinstance(s1, int) and isinstance(s2, list):
		return cmp_signals([s1], s2)

	if isinstance(s1, int) and isinstance(s2, int):
		return s1 - s2
	
	for sp1, sp2 in itertools.zip_longest(s1, s2):
		if sp1 is None:
			return -1
		
		if sp2 is None:
			return 1
		
		current_cmp = cmp_signals(sp1, sp2)
		if current_cmp == 0:
			continue

		return current_cmp
	
	return 0


def part1(signals: list[list]) -> int:
	return sum(
		index + 1
		for index, signal_pair in enumerate(chunk(signals, 2))
		if cmp_signals(*signal_pair) <= 0
	)

def part2(signals: list[list]) -> int:
	signals_with_dividers = signals + [[[2]], [[6]]]
	sorted_signals = sorted(
		signals_with_dividers,
		key=functools.cmp_to_key(cmp_signals),
	)

	return (sorted_signals.index([[2]]) + 1) * (sorted_signals.index([[6]]) + 1)
