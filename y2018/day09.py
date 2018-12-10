import re

def preprocess_input(lines):
	return map(int, re.findall("\d+", lines[0]))

def part1(stats):
	num_players, last_marble = stats

	player_scores = [0]*num_players
	marbles = [0]

	marble_num = 0
	last_ind = 0

	while True:
		for player in range(len(player_scores)):
			marble_num += 1
			if marble_num % 23 == 0:
				omarble_ind = (last_ind - 7) % len(marbles)
				player_scores[player] += marble_num + marbles[omarble_ind]

				del marbles[omarble_ind]
				last_ind = omarble_ind
			
			else:
				last_ind = (last_ind + 2) % len(marbles)
				marbles.insert(last_ind, marble_num)

			if marble_num >= last_marble:
				return max(player_scores)
				

def part2(stats):
	num_players, last_marble = stats
	return part1((num_players, last_marble*100))

