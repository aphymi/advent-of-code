"""
This module provides functions for extracting relevant information from
challenge input files, originally formatted as a list of strings, one for each
line in the input.
"""

from typing import (Callable, Iterable, List, Pattern, Sequence, Tuple, TypeVar,
	Union)
import re

def compose(*functions: Callable) -> Callable:
	"""
	Compose several functions, so that the output for one is the input for the
	next.
	
	The first argument receives the original input, the second receives the
	first's output, the third receives the second's output, etc.
	
	Args:
		*functions: Several functions to be applied in left-to-right order.
	
	Returns:
		The resulting composed function.
	"""
	
	def composed(inp):
		last_output = inp
		for op in functions:
			last_output = op(last_output)
		return last_output
	
	return composed

def parallel(*functions: Callable) -> Callable[..., List[Tuple]]:
	"""
	Compose several functions parallelly, so that the resulting output for each
	line is a tuple with one item for the output of each argument function.
	
	Examples:
	>>> plus1 = lambda x: x+1
	>>> plus2 = lambda x: x+2
	>>> plus3 = lambda x: x+3
	>>> paralleled = parallel(plus1, plus2, plus3)
	>>> data = [0, 100, 333]
	>>> paralleled(data)
	[(1,2,3), (101, 102, 103), (334, 335, 336)]
	
	Args:
		*functions: Several to apply in parallel.
	
	Returns:
		The resulting parallelly-composed function.
	"""
	
	def paralleled(inp):
		return list(zip(*[op(inp) for op in functions]))
	
	return paralleled

def parallel_tuple(*functions: Callable) -> Callable[..., List[Tuple]]:
	"""
	Compose several functions parallelly, so that each is applied to the
	corresponding item in the sequence of input.

	Examples:
	>>> plus1 = lambda x: x+1
	>>> plus2 = lambda x: x+2
	>>> plus3 = lambda x: x+3
	>>> paralleled = parallel_tuple(plus1, plus2, plus3)
	>>> data = [(0, 1, 2), (101, 102, 103)]
	>>> paralleled(data)
	[(1, 3, 5), (102, 104, 106)]
	"""

	def paralleled(inp):
		new_lines = []
		for line in inp:
			new_line = tuple(
				func(line_part)
				for func, line_part in zip(functions, line)
			)
			new_lines.append(new_line)
		return new_lines
	
	return paralleled

def zip_input_with(*functions: Callable) -> Callable[[Iterable], List]:
	"""
	Create a function which applies the given functions across an iterable
	input.

	Examples:
	>>> plus1 = lambda x: x+1
	>>> plus2 = lambda x: x+2
	>>> plus3 = lambda x: x+3
	>>> zipped = zip_input_with(plus1, plus2, plus3)
	>>> data = [0, 0, 0]
	>>> zipped(data)
	[1, 2, 3]
	"""
	def zipped(inp):
		return [
			func(inp_part)
			for func, inp_part in zip(functions, inp)
		]
	
	return zipped

def split(lines: Iterable[str]) -> List[List[str]]:
	"""
	Return the result of mapping str.split() onto every item in the argument.
	"""
	
	return [line.split() for line in lines]

def split_on(spl: str = None) -> List[List[str]]:
	"""
	Return a function that maps str.split(spl) onto every item in its input.
	"""
	
	def splitted(lines):
		return [line.split(spl) for line in lines]
	
	return splitted

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")
def map_func(
	func: Callable[[TIn], TOut],
) -> Callable[[Iterable[TIn]], List[TOut]]:
	"""
	Return a function that maps func onto every item of its input.
	"""

	def mapped(inp):
		return [func(line) for line in inp]
	
	return mapped

T = TypeVar("T")
def single_line(lines: Sequence[T]) -> T:
	"""
	Return the first item of the input.
	"""
	
	return lines[0]

def joined_line(lines: Iterable[str]) -> str:
	"""
	Return the input, all joined into a single line with newlines.
	"""

	return "\n".join(lines)

def get_regex_matches(
	regex: Union[str, Pattern],
) -> Callable[[Iterable[str]], List[List[str]]]:
	"""
	Return a function that finds all regex matches on each line of its input.
	
	Args:
		The regular expression to match on each line.
	"""
	
	return map_func(lambda line: re.findall(regex, line))

def get_ints(lines: Iterable[str]) -> List[List[int]]:
	"""
	Return the result of mapping an integer-finding function onto each item in
	the input.
	"""
	
	return [
		[int(m) for m in line]
		for line in get_regex_matches(r"-?\d+")(lines)
	]

def get_pos_ints(lines: Iterable[str]) -> List[List[int]]:
	"""
	Return the result of mapping a positive integer-finding function onto each
	item in the input.
	
	This function specifically ignores negative integers, so that it may find
	numbers which may be preceded by a dash which is not meant to symbolise a
	negative sign (e.g. gets both 10 and 99 from "10-99").
	"""
	
	return [
		[int(m) for m in line]
		for line in get_regex_matches(r"\d+")(lines)
	]
