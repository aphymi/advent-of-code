from util.parse import *


parse_input = compose(
	get_regex_matches("\d{1,2}$"),
	lambda lines: [int(line[0]) for line in lines],
	tuple,
)

PlayPosition = int
PlayerPositions = tuple[PlayPosition, PlayPosition]

class DeterministicDie:
	times_rolled = 0

	def roll(self) -> int:
		value = (self.times_rolled % 100) + 1
		self.times_rolled += 1
		return value

def get_new_position(old_position: int, move: int) -> int:
	return (
		((old_position - 1) + move) % 10
	) + 1

def play_game(starting_positions: PlayerPositions):
	positions = {
		"left": starting_positions[0],
		"right": starting_positions[1],
	}

	scores = {
		"left": 0,
		"right": 0,
	}

	die = DeterministicDie()

	turn = "left"

	while all(score < 1000 for score in scores.values()):
		old_pos = positions[turn]

		move_value = sum(
			die.roll()
			for _i in range(3)
		)

		new_pos = get_new_position(old_pos, move_value)

		positions[turn] = new_pos
		scores[turn] += new_pos
		turn = "right" if turn == "left" else "left"

	return min(scores.values()) * die.times_rolled

def play_quantum_game(
	positions: dict[str, int],
	scores: dict[str, int] = {"left": 0, "right": 0},
	turn = "left",
	depth = 0,
) -> dict[str, int]:
	move_weights = {
		3: 1,
		4: 3,
		5: 6,
		6: 7,
		7: 6,
		8: 3,
		9: 1,
	}

	wins = {
		"left": 0,
		"right": 0,
	}

	for move, weight in move_weights.items():
		new_positions = positions.copy()
		new_scores = scores.copy()
		new_positions[turn] = get_new_position(positions[turn], move)
		new_scores[turn] += new_positions[turn]


		if new_scores[turn] >= 21:
			wins[turn] += weight
		
		else:
			latest_wins = play_quantum_game(
				new_positions,
				new_scores,
				"right" if turn == "left" else "left",
				depth + 1,
			)
			wins["left"] += latest_wins["left"] * weight
			wins["right"] += latest_wins["right"] * weight

	return wins


def part1(positions: PlayerPositions) -> int:
	return play_game(positions)

def part2(positions: PlayerPositions) -> int:
	wins = play_quantum_game(
		{
			"left": positions[0],
			"right": positions[1],
		},
	)

	return max(wins.values())
