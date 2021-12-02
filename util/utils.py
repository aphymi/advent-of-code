from collections import deque
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


if __name__ == "__main__":
	print(list(sliding_window(range(10), 3)))
