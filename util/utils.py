from collections import deque
import itertools
from typing import Generator, Iterable, Tuple, TypeVar


X = TypeVar("X")
def sliding_window(
	iterable: Iterable[X],
	window_size: int = 2
) -> Generator[Tuple[X], None, None]:
	last_n = deque()
	iterator = iter(iterable)

	for item in iterator:
		last_n.append(item)

		if (len(last_n) < window_size):
			continue

		yield tuple(last_n)

		last_n.popleft()

def flatten(
	iterable_of_iterables: Iterable[Iterable[X]],
) -> Generator[X, None, None]:
	for iterable in iterable_of_iterables:
		for item in iterable:
			yield item

def ceildiv(a: int, b: int) -> int:
	return -(a // -b)

def manhattan_distance(a: Iterable[float], b: Iterable[float]) -> float:
	return sum(
		abs(a_part - b_part)
		for a_part, b_part in zip(a, b)
	)

def pairwise(iterable: Iterable[X]) -> Generator[Tuple[X, X], None, None]:
	"""
	Return successive overlapping pairs taken from the input iterable.

	Equivalent to Python3.10's `itertools.pairwise`, for use in earlier python
	versions.
	"""
	a, b = itertools.tee(iterable)
	next(b, None)
	return zip(a, b)


def chunk(
	iterable: Iterable[X],
	chunk_size: int,
) -> Generator[tuple[X], None, None]:
	"""
	Split an iterable into chunks of the given size.

	>>> list(chunk([1,2,3,4,5,6,7,8,9], 3))
	[[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	"""

	current_chunk = []
	for item in iterable:
		if len(current_chunk) >= chunk_size:
			yield tuple(current_chunk)
			current_chunk = []
		
		current_chunk.append(item)
	
	if len(current_chunk) > 0:
		yield tuple(current_chunk)


if __name__ == "__main__":
	print(list(sliding_window(range(10), 3)))
