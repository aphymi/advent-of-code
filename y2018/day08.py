from util.parse import *

def build_nodes(nums):
	num_children = nums.pop()
	num_meta = nums.pop()
	return {
		"children": [build_nodes(nums) for _ in range(num_children)],
		"meta": [nums.pop() for _ in range(num_meta)]
	}

parse_input = compose(
	get_ints,
	single_line,
	reversed,
	list,
	build_nodes,
)

def part1(root):
	def sums(node):
		return sum(node["meta"]) + sum([sums(child) for child in node["children"]])
	
	return sums(root)

def part2(root):
	def values(node):
		if not node["children"]:
			return sum(node["meta"])
		
		return sum([values(node["children"][i-1]) for i in node["meta"] if i <= len(node["children"])])
	
	return values(root)
