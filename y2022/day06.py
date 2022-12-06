from util.parse import *
from util.utils import sliding_window


parse_input = compose(
	single_line,
)

def get_num_for_distinct_characters(
	data_stream: str,
	distinct_characters: int,
) -> int:
	latest_character_number = distinct_characters
	for window in sliding_window(data_stream, distinct_characters):
		if len(set(window)) == distinct_characters:
			return latest_character_number
		
		latest_character_number += 1
	
	raise Exception(
		f"Cannot find a run of {distinct_characters} distinct characters",
	)


def part1(data_stream: str) -> int:
	return get_num_for_distinct_characters(data_stream, 4)

def part2(data_stream: str) -> int:
	return get_num_for_distinct_characters(data_stream, 14)
