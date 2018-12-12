import json
import re

def preprocess_input(lines):
	return "".join(lines)

def part1(doc):
	return sum(map(int, re.findall("-?\d+", doc)))

def part2(doc):
	def sum_tree(item):
		if isinstance(item, int):
			return item
		elif isinstance(item, list):
			return sum(sum_tree(i) for i in item)

		elif isinstance(item, dict) and "red" not in item.values():
			return sum(sum_tree(item[k]) for k in item)
		
		return 0
	
	return sum_tree(json.loads(doc))

