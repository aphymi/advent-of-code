def preprocess_input(lines):
	nums = list(map(int, reversed(lines[0].split())))
	
	def build_nodes():
		num_children = nums.pop()
		num_meta = nums.pop()
		return {
			"children": [build_nodes() for _ in range(num_children)],
			"meta": [nums.pop() for _ in range(num_meta)]
		}
	
	return build_nodes()

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
