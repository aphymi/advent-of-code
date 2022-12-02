from util.parse import *


parse_input = compose(
	map_func(lambda line: tuple(line.split(" "))),
)

RoundGuide = tuple[str, str]

# for a given index i, i+1 beats i, and i beats i-1
# (all % 3)
move_dominance = ["A", "B", "C"]

def get_round_score(opponent_move: str, player_move: str) -> int:
	opponent_move_index = move_dominance.index(opponent_move)
	player_move_index = move_dominance.index(player_move)

	if opponent_move_index == player_move_index:
		return 3 + player_move_index + 1
	
	elif opponent_move_index == ((player_move_index - 1) % len(move_dominance)):
		return 6 + player_move_index + 1
	
	else:
		return player_move_index + 1

def get_responding_move(round_guide: RoundGuide) -> str:
	opponent_move, desired_result = round_guide

	result_offsets = {
		"X": -1,
		"Y": 0,
		"Z": 1,
	}

	player_move_index = (
		move_dominance.index(opponent_move)
		+ result_offsets[desired_result]
	) % len(move_dominance)

	return move_dominance[player_move_index]

def part1(strategy_guide: list[RoundGuide]) -> int:
	translation = {
		"X": "A",
		"Y": "B",
		"Z": "C",
	}

	return sum(
		get_round_score(round_guide[0], translation[round_guide[1]])
		for round_guide in strategy_guide
	)

def part2(strategy_guide: list[RoundGuide]) -> int:
	return sum(
		get_round_score(round_guide[0], get_responding_move(round_guide))
		for round_guide in strategy_guide
	)
