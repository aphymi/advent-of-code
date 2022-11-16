import heapq
from typing import Generator, Optional

from util.parse import *


class AmphipodPosition:
	room_contents: list[list[Optional[int]]]
	hallway_contents = [None] * 11
	cumulative_energy = 0
	previous = None

	room_positions = [2, 4, 6, 8]
	room_types_to_positions = {
		"A": 2,
		"B": 4,
		"C": 6,
		"D": 8,
	}
	room_positions_to_types = {
		2: "A",
		4: "B",
		6: "C",
		8: "D",
	}

	def __init__(
		self,
		room_contents,
		hallway_contents = None,
		cumulative_energy = None,
		previous = None,
	) -> None:
		self.room_contents = room_contents
		
		if hallway_contents is not None:
			self.hallway_contents = hallway_contents
		
		if cumulative_energy is not None:
			self.cumulative_energy = cumulative_energy

		self.previous = previous
	
	def __repr__(self) -> str:
		return f"AmphipodPosition(room_contents={self.room_contents},hallway_contents={self.hallway_contents},cumulative_energy={self.cumulative_energy})"

	def __hash__(self) -> int:
		return hash(
			tuple(self.hallway_contents)
		) ^ hash(
			tuple(
				tuple(room) for room in self.room_contents
			)
		)
	
	def __eq__(self, other) -> bool:
		return (
			self.hallway_contents == other.hallway_contents
			and self.room_contents == other.room_contents
		)
	
	def __lt__(self, other) -> bool:
		return self.cumulative_energy < other.cumulative_energy
	
	def is_sorted(self) -> bool:
		room_keys = self.room_types_to_positions.keys()
		return all(
			all(space == amphipod_type for space in room)
			for amphipod_type, room in zip(room_keys, self.room_contents)
		)
	
	def get_history(self) -> list["AmphipodPosition"]:
		history = [self]
		cur = self
		while cur.previous is not None:
			cur = cur.previous
			history.append(cur)
		
		history.reverse()
		return history
	
	def print(self) -> None:
		print("#" * 13)
		print("#" + "".join(c or "." for c in self.hallway_contents) + "#")
		zipped_hallways = list(zip(*self.room_contents))
		for index, hallway_layer in enumerate(zipped_hallways):
			filler = "###" if index == 0 else "  #"
			reversed_filler = "".join(reversed(filler))

			print(filler, end="")
			print("#".join(c or "." for c in hallway_layer), end="")
			print(reversed_filler)
		print("  " + "#"*9)
		print(f"({self.cumulative_energy})")

	def get_next_positions(
		self,
	) -> Generator["AmphipodPosition", None, None]:
		for index, item in enumerate(self.hallway_contents):
			if item is not None:
				yield from self.get_possible_moves_from_hallway(index)
		
		for room_index, room in enumerate(self.room_contents):
			for index_within_room, space_within_room in enumerate(room):
				if space_within_room is not None:
					yield from self.get_possible_moves_from_room(
						room_index,
						index_within_room,
					)
		
	def get_possible_moves_from_hallway(
		self,
		current_hallway_index: int,
	) -> Generator["AmphipodPosition", None, None]:
		open_hallway_indices = self.get_open_hallway_indices_from(
			current_hallway_index,
		)
		current_amphipod_type = self.hallway_contents[current_hallway_index]
		for open_hallway_index in open_hallway_indices:
			if open_hallway_index not in self.room_positions:
				continue

			room_amphipod_type = (
				self.room_positions_to_types[open_hallway_index]
			)
			if current_amphipod_type != room_amphipod_type:
				continue

			room_index = self.room_positions.index(open_hallway_index)
			room = self.room_contents[room_index]
			room_has_no_unsorted = all(
				room_item is None or room_item == room_amphipod_type
				for room_item in room
			)

			if not room_has_no_unsorted:
				continue

			steps_to_outside_room = abs(
				current_hallway_index - open_hallway_index,
			)
			cleared_hallway = self.hallway_contents.copy()
			cleared_hallway[current_hallway_index] = None
			for index, space in enumerate(room):
				if space is not None:
					# Can't go any further into room
					break
				
				new_room = ([None] * (index)) + room[index:]
				new_room[index] = current_amphipod_type

				new_room_contents = self.room_contents.copy()
				new_room_contents[room_index] = new_room

				steps_into_room = index + 1
				steps = steps_to_outside_room + steps_into_room
				move_energy = steps * self.get_step_cost(current_amphipod_type)

				new_position = AmphipodPosition(
					hallway_contents=cleared_hallway,
					room_contents=new_room_contents,
					cumulative_energy=self.cumulative_energy + move_energy,
					previous=self,
				)
				yield new_position
	
	def get_possible_moves_from_room(
		self,
		room_index: int,
		amphipod_index_in_room: int,
	) -> Generator["AmphipodPosition", None, None]:
		room = self.room_contents[room_index]

		# Check if this amphipod is blocked from exiting
		if any(space is not None for space in room[:amphipod_index_in_room]):
			return

		new_room = room.copy()
		new_room[amphipod_index_in_room] = None

		new_room_contents = self.room_contents.copy()
		new_room_contents[room_index] = new_room

		amphipod_type = room[amphipod_index_in_room]
		hallway_index = self.room_positions[room_index]

		open_hallway_indices = self.get_open_hallway_indices_from(
			hallway_index,
		)

		for open_hallway_index in open_hallway_indices:
			if open_hallway_index in self.room_positions:
				continue
			
			steps_out_of_room = amphipod_index_in_room + 1
			steps_through_hallway = abs(hallway_index - open_hallway_index)
			steps = steps_out_of_room + steps_through_hallway
			move_energy = steps * self.get_step_cost(
				amphipod_type,
			)

			new_hallway = self.hallway_contents.copy()
			new_hallway[open_hallway_index] = amphipod_type

			new_position = AmphipodPosition(
				hallway_contents=new_hallway,
				room_contents=new_room_contents,
				cumulative_energy=self.cumulative_energy + move_energy,
				previous=self,
			)
			yield new_position

	def get_open_hallway_indices_from(self, from_index: int) -> list[int]:
		open_indices = []

		# Try left from index
		for index in range(from_index - 1, -1, -1):
			if self.hallway_contents[index] is not None:
				break

			open_indices.append(index)
		
		# Try right from index
		for index in range(from_index + 1, len(self.hallway_contents)):
			if self.hallway_contents[index] is not None:
				break

			open_indices.append(index)
		
		return open_indices
	
	def get_step_cost(self, amphipod_type: str) -> int:
		if amphipod_type == "A":
			return 1
		
		if amphipod_type == "B":
			return 10

		if amphipod_type == "C":
			return 100
		
		if amphipod_type == "D":
			return 1000

parse_input = compose(
	lambda lines: lines[2:4],
	get_regex_matches(r"[ABCD]"),
	lambda lines: list(list(line) for line in zip(*lines)),
	lambda room_positions: AmphipodPosition(room_contents=room_positions),
)

def sort_amphipods(start_position: AmphipodPosition) -> AmphipodPosition:
	queue = [start_position]
	seen = set()

	while len(queue) > 0:
		cur = heapq.heappop(queue)
		
		if cur in seen:
			continue
		seen.add(cur)

		if cur.is_sorted():
			return cur

		for next_pos in cur.get_next_positions():
			heapq.heappush(queue, next_pos)

def print_history(history: list[AmphipodPosition]) -> None:
	for position in history:
		position.print()
		print("-------------")

def part1(start_position: AmphipodPosition) -> int:
	sorted_position = sort_amphipods(start_position)

	return sorted_position.cumulative_energy

def part2(start_position: AmphipodPosition) -> int:
	room_layers = list(zip(*start_position.room_contents))
	new_room_layers = [
		list(room_layers[0]),
		["D", "C", "B", "A"],
		["D", "B", "A", "C"],
		list(room_layers[1]),
	]
	unfolded_position = AmphipodPosition(
		room_contents=list(list(hallway) for hallway in zip(*new_room_layers)),
		hallway_contents=start_position.hallway_contents
	)
	
	sorted_position = sort_amphipods(unfolded_position)
	# print_history(sorted_position.get_history())
	return sorted_position.cumulative_energy
