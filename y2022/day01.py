from util.parse import *


parse_input = compose(
	joined_line,
	lambda inp: inp.split("\n\n"),
	lambda str_calorie_groups: [
		[int(calories) for calories in calorie_group.split("\n")]
		for calorie_group in str_calorie_groups
	],
)

CalorieGroup = list[int]

def part1(calorie_groups: list[CalorieGroup]) -> int:
	return max(
		sum(calorie_group) for calorie_group in calorie_groups
	)

def part2(calorie_groups: list[CalorieGroup]) -> int:
	return sum(
		sum(calorie_group)
		for calorie_group in sorted(calorie_groups, key=sum)[-3:]
	)
