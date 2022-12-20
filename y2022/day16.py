import functools

from util.parse import *


valve_counter = 0

class Valve:
	name: str
	flow_rate: int
	connections: tuple[str, ...]
	bit_flag: int = None
	hash: int

	def __init__(
		self,
		name: str,
		flow_rate: int,
		connections: tuple[str, ...],
	) -> None:
		self.name = name
		self.flow_rate = flow_rate
		self.connections = connections
		self.hash = hash(self.name)

		global valve_counter
		self.bit_flag = 1 << valve_counter
		valve_counter += 1
	
	def __repr__(self) -> str:
		return (
			f"Valve(name={repr(self.name)}, "
			f"flow_rate={self.flow_rate}, "
			f"connections={repr(self.connections)})"
		)
	
	def __hash__(self) -> int:
		return self.hash

	def __lt__(self, other) -> bool:
		return self.name < other.name

parse_input = compose(
	split_on(" "),
	map_func(
		lambda line: Valve(
			name=line[1],
			flow_rate=int(line[4][5:-1]),
			connections=tuple(
				[valve_name[:-1] for valve_name in line[9:-1]]
				+ [line[-1]]
			),
		),
	),
)

valve_map = None

@functools.cache
def get_optimal_released_pressure(
	valves: tuple[Valve],
	current_valve: Valve,
	time: int,
	opened_valves: frozenset[str],
	other_players: int = 0,
	start_valve: Valve = None,
	start_time: int = None,
) -> int:
	if time == 0:
		if other_players > 0:
			return get_optimal_released_pressure(
				valves,
				start_valve,
				start_time,
				opened_valves,
				other_players - 1,
				start_valve,
				start_time,
			)

		return 0
	
	global valve_map
	if valve_map is None:
		valve_map = {valve.name: valve for valve in valves}

	self_open_value = float("-inf")
	if current_valve.name not in opened_valves and current_valve.flow_rate > 0:
		pressure_released = (time - 1) * current_valve.flow_rate

		self_open_value = pressure_released + get_optimal_released_pressure(
			valves,
			current_valve,
			time - 1,
			opened_valves.union({current_valve.name}),
			other_players,
			start_valve,
			start_time,
		)

	best_connection = max(
		get_optimal_released_pressure(
			valves,
			valve_map[valve_name],
			time - 1,
			opened_valves,
			other_players,
			start_valve,
			start_time,
		)
		for valve_name in current_valve.connections
	)

	return max(self_open_value, best_connection)

def part1(valves: list[Valve]) -> int:
	start_valve = next(
		valve for valve in valves if valve.name == "AA"
	)

	return get_optimal_released_pressure(
		tuple(valves),
		start_valve,
		30,
		frozenset(),
	)

def part2(valves: list[Valve]) -> int:
	start_valve = next(
		valve for valve in valves if valve.name == "AA"
	)

	return get_optimal_released_pressure(
		tuple(valves),
		start_valve,
		26,
		frozenset(),
		1,
		start_valve,
		26,
	)
