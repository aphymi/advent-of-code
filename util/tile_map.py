from typing import Generator, Generic, TypeVar


T = TypeVar("T")
TileData = tuple[T, int, int]

class TileMap(Generic[T]):
	"""
	A two dimensional grid of a generic type.
	"""

	def __init__(self, state: list[list[T]]) -> None:
		self.state = state
	
	def get_at(self, x: int, y: int) -> T:
		"""
		Return the value at the given x and y coordinates.
		"""

		return self.state[y][x]

	def walk(self) -> Generator[TileData, None, None]:
		"""
		Generate a complete enumeration of the map's state.

		Starts in the top left (x=0, y=0), goes left to right, then up-to-down.
		"""

		for y, row in enumerate(self.state):
			for x, value in enumerate(row):
				yield (value, x, y)

	def get_adjacent_4(self, x: int, y: int) -> Generator[TileData, None, None]:
		"""
		Generate an enumeration of the tiles directly adjacent to x and y.
		"""

		modifiers = [
			(0, -1),
			(-1, 0),
			(1, 0),
			(0, 1),
		]

		adjacent = []
		for modifier in modifiers:
			adj_x = x + modifier[0]
			adj_y = y + modifier[1]
				
			if adj_y not in range(len(self.state)):
				continue

			if adj_x not in range(len(self.state[adj_y])):
				continue
				
			yield (
				self.state[adj_y][adj_x],
				adj_x,
				adj_y
			)
