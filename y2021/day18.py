import copy
import dataclasses
import functools
import itertools
import math
import typing

from util.parse import *


parse_input = map_func(eval)

SnailfishNumber = typing.Union[int, list]

@dataclasses.dataclass
class ReduceResult:
	result: SnailfishNumber
	left_explode: typing.Optional[int]
	right_explode: typing.Optional[int]
	reduced: bool

def add_exploded(
	exploded_num: int,
	cur_number: SnailfishNumber,
	left: bool,
) -> bool:
	explode_index = 0 if left else 1
	if type(cur_number[explode_index]) == int:
		cur_number[explode_index] += exploded_num
	else:
		add_exploded(exploded_num, cur_number[explode_index], left)

def reduce_recur(
	sf_num: SnailfishNumber,
	depth: int = 0,
	allow_splits = True,
) -> ReduceResult:
	if type(sf_num) == int:
		if sf_num >= 10 and allow_splits:
			split_pair = [
				sf_num // 2,
				math.ceil(sf_num / 2),
			]
			allow_splits = False
			
			return ReduceResult(
				split_pair,
				None,
				None,
				True,
			)
		
		return ReduceResult(
			result = sf_num,
			left_explode = None,
			right_explode = None,
			reduced = False,
		)
	
	# type(sf_num) == list
	if depth >= 4:
		return ReduceResult(
			0,
			sf_num[0],
			sf_num[1],
			True
		)
	
	left_result = reduce_recur(sf_num[0], depth + 1, allow_splits)
	if left_result.right_explode is not None:
		if type(sf_num[1]) == int:
			sf_num[1] += left_result.right_explode
		else:
			add_exploded(
				left_result.right_explode,
				sf_num[1],
				True,
			)

	if left_result.reduced:
		return ReduceResult(
			[left_result.result, sf_num[1]],
			left_result.left_explode,
			0,
			True,
		)
	
	right_result = reduce_recur(sf_num[1], depth + 1, allow_splits)
	if right_result.left_explode is not None:
		if type(sf_num[0]) == int:
			sf_num[0] += right_result.left_explode
		else:
			add_exploded(
				right_result.left_explode,
				sf_num[0],
				False,
			)
	
	if right_result.reduced:
		return ReduceResult(
			[sf_num[0], right_result.result],
			0,
			right_result.right_explode,
			True,
		)

	return ReduceResult(
		[left_result.result, right_result.result],
		left_result.left_explode,
		right_result.right_explode,
		left_result.reduced or right_result.reduced,
	)

def reduce(sf_num: SnailfishNumber) -> SnailfishNumber:
	current_sf_num = copy.deepcopy(sf_num)
	allow_splits = False
	n = 1

	while True:
		result = reduce_recur(current_sf_num, allow_splits=allow_splits)

		current_sf_num = result.result

		reduced = result.reduced

		if reduced:
			n += 1

		if not reduced:
			if allow_splits:
				break

			allow_splits = True
		
		else:
			if allow_splits:
				allow_splits = False

	
	return current_sf_num

def get_magnitude(sf_num: SnailfishNumber) -> int:
	if type(sf_num) == int:
		return sf_num
	
	return get_magnitude(sf_num[0])*3 + get_magnitude(sf_num[1])*2

def part1(sf_nums: list[SnailfishNumber]) -> int:
	if len(sf_nums) == 1:
		final_result = reduce(sf_nums[0])

	else:
		final_result = functools.reduce(
			lambda cumu, next: reduce([cumu, next]),
			sf_nums,
		)

	return get_magnitude(final_result)

def part2(sf_nums: list[SnailfishNumber]) -> int:
	return max(
		get_magnitude(reduce([sf1, sf2]))
		for sf1, sf2 in itertools.permutations(sf_nums, 2)
	)
