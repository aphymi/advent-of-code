import collections

from util.parse import *
from util import utils


PolymerRules = dict[str, str]
TemplateAndRules = tuple[str, PolymerRules]

def parse_input(lines: list[str]) -> tuple[str, PolymerRules]:
	template = lines[0]
	rules = dict(
		rule_line.split(" -> ")
		for rule_line in lines[2:]
	)

	return (template, rules)

def react_polymer(
	template: str,
	rules: PolymerRules,
	times: int,
) -> dict[str, int]:
	pair_counts = collections.Counter(
		"".join(characters)
		for characters in utils.sliding_window(template, 2)
	)

	for _i in range(times):
		new_pair_counts = collections.defaultdict(int)

		for pair, count in pair_counts.items():
			if pair in rules:
				new_reactant = rules[pair]
				new_pair_counts[pair[0] + new_reactant] += count
				new_pair_counts[new_reactant + pair[1]] += count
			else:
				print("no")
				new_pair_counts[pair] += count
		
		pair_counts = new_pair_counts
	
	character_counts = collections.defaultdict(int)
	character_counts[template[-1]] = 1

	for pair, count in pair_counts.items():
		character_counts[pair[0]] += count
	
	return character_counts


def part1(template_and_rules: TemplateAndRules) -> int:
	template, rules = template_and_rules

	character_counts = react_polymer(template, rules, 10)

	return max(character_counts.values()) - min(character_counts.values())

def part2(template_and_rules: TemplateAndRules) -> int:
	template, rules = template_and_rules

	character_counts = react_polymer(template, rules, 40)

	return max(character_counts.values()) - min(character_counts.values())
