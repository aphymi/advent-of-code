from enum import Enum

from util.parse import *
from util.tile_map import TileMap


parse_input = lambda lines: (
	lines[0],
	TileMap([list(line) for line in lines[2:]]),
)

Image = TileMap[str]
class FieldState(Enum):
	DARK = "dark"
	LIT = "lit"

def get_enhancement_index(
	input_image: Image,
	x: int,
	y: int,
	field_state: FieldState,
) -> int:
	filler_pixel = "#" if field_state == FieldState.LIT else "."
	self_pixel = input_image.get_at(x, y, safe=True) or filler_pixel

	adjacent_pixels = list(
		value or filler_pixel
		for value, _x, _y in input_image.get_adjacent_8(
			x,
			y,
			include_out_of_bounds=True,
		)
	)

	bits_in_order = adjacent_pixels[:4]  + [self_pixel] + adjacent_pixels[4:]
	pixel_string = "".join(bits_in_order)
	bitstring = "".join("1" if pixel == "#" else "0" for pixel in pixel_string)

	return int(bitstring, 2)

def enhance_image(
	input_image: Image,
	enhancement_string: str,
	iterations: int,
) -> Image:
	current_image = input_image
	field_state = FieldState.DARK
	field_state_swaps = enhancement_string[0] == "#"

	for _i in range(iterations):
		rows = []
		for y in range(-1, current_image.get_height() + 1):
			row = []
			for x in range(-1, current_image.get_width() + 1):
				enhancement_index = get_enhancement_index(
					current_image,
					x,
					y,
					field_state,
				)

				row.append(enhancement_string[enhancement_index])

			rows.append(row)
		
		current_image = TileMap(rows)
		if field_state_swaps:
			field_state = FieldState.LIT if field_state == FieldState.DARK else FieldState.DARK
	
	return current_image

Input = tuple[str, Image]

def print_image(image: Image, field_is_lit: bool = False) -> None:
	min_size = 110

	y_padding = (min_size - image.get_height()) // 2
	x_padding = (min_size - image.get_width()) // 2
	padding_char = "#" if field_is_lit else "."

	for _i in range(y_padding):
		print(padding_char * min_size)
	
	for row in image.state:
		print(padding_char * x_padding, end="")
		print("".join(row), end="")
		print(padding_char * x_padding)
		
	for _i in range(y_padding):
		print(padding_char * min_size)

def part1(input_tuple: Input) -> int:
	enhancement_string, input_image = input_tuple

	end_image = enhance_image(input_image, enhancement_string, 2)

	light_pixels = sum(
		1 if value == "#" else 0
		for value, _x, _y in end_image.walk()
	)
	
	return light_pixels

def part2(input_tuple: Input) -> int:
	enhancement_string, input_image = input_tuple

	end_image = enhance_image(input_image, enhancement_string, 50)

	light_pixels = sum(
		1 if value == "#" else 0
		for value, _x, _y in end_image.walk()
	)
	
	return light_pixels
