from typing import Generator


def get_dir_in_dir_tree(dir_tree: dict, wd: list) -> dict:
	"""
	Get the directory dict for the given working directory.

	Creates said directory in the dir tree if it doesn't exist.
	"""

	current_directory = dir_tree

	for directory in wd:
		if directory not in current_directory["dirs"]:
			current_directory["dirs"][directory] = {
				"files": {},
				"dirs": {},
			}
		
		current_directory = current_directory["dirs"][directory]
	
	return current_directory

def construct_dir_structure(terminal_output: list[str]) -> dict:
	cwd = []
	current_directory = {
		"files": {},
		"dirs": {},
	}
	dir_tree = current_directory

	for line in terminal_output:
		if line == "$ cd /":
			cwd = []
		
		elif line == "$ cd ..":
			cwd.pop()
		
		elif line.startswith("$ cd "):
			cwd.append(line.split()[2])

		elif line == "$ ls":
			# We ignore ls itself, and assume its output when a line doesn't
			# start with $
			pass
		
		elif line.startswith("dir "):
			# We ignore listed directories
			pass

		else:
			file_length, filename = line.split()
			current_directory["files"][filename] = int(file_length)

		current_directory = get_dir_in_dir_tree(dir_tree, cwd)
	
	return dir_tree

def walk_dirs(
	dir_tree: dict,
) -> Generator[tuple[dict, dict, int], None, int]:
	total_size = 0
	for dir in dir_tree["dirs"].values():
		total_size += yield from walk_dirs(dir)
	
	total_size += sum(dir_tree["files"].values())
	
	yield (dir_tree["dirs"], dir_tree["files"], total_size)

	return total_size

def part1(terminal_output: list[str]) -> int:
	dir_tree = construct_dir_structure(terminal_output)

	return sum(
		dir_size
		for _dirs, _files, dir_size in walk_dirs(dir_tree)
		if dir_size <= 10**5
	)

def part2(terminal_output: list[str]) -> int:
	dir_tree = construct_dir_structure(terminal_output)

	# Not a very efficient way to get this, but it's easy
	total_used_space = max(
		dir_size
		for _dirs, _files, dir_size in walk_dirs(dir_tree)
	)

	space_needed = total_used_space - 40 * 10**6

	return min(
		dir_size
		for _dirs, _files, dir_size in walk_dirs(dir_tree)
		if dir_size >= space_needed
	)
