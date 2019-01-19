from collections import deque

from util.parse import *
parse_input = compose(single_line, get_ints)

def max_marble_score(num_players, last_marble):
	player_scores = [0]*num_players
	marbles = deque([0])

	marble_num = 0

	while True:
		for player in range(len(player_scores)):
			marble_num += 1
			if marble_num % 23 == 0:
				marbles.rotate(7)
				player_scores[player] += marble_num + marbles.popleft()
			
			else:
				marbles.rotate(-2)
				marbles.appendleft(marble_num)

			if marble_num >= last_marble:
				return max(player_scores)

def part1(stats):
	return max_marble_score(*stats)
	
def part2(stats):
	num_players, last_marble = stats
	return max_marble_score(num_players, last_marble*100)

