from typing import List

from util.parse import *

image_dimensions = (25, 6)

def parse_input(lines):
	image_data = lines[0]
	pixels_in_layer = image_dimensions[0] * image_dimensions[1]
	
	return [
		image_data[i: i+pixels_in_layer]
		for i in range(0, len(image_data), pixels_in_layer)
	]

ImageLayers = List[str]

def part1(layers: ImageLayers) -> int:
	fewest_zeroes_layer = min(
		layers,
		key=lambda l: l.count("0"),
	)
	
	return fewest_zeroes_layer.count("1") * fewest_zeroes_layer.count("2")

print_chars = {
	"0": " ",
	"1": "H",
}

def part2(layers: ImageLayers) -> None:
	final_pixels = []
	
	for pixel_index in range(len(layers[0])):
		for layer in layers:
			if layer[pixel_index] != "2":
				final_pixels.append(layer[pixel_index])
				break
		else:
			final_pixels.append("2")
	
	for i, pixel_code in enumerate(final_pixels):
		final_pixels[i] = print_chars[pixel_code]
		
	for i in range(0, len(final_pixels), image_dimensions[0]):
		print("".join(final_pixels[i:i+image_dimensions[0]]))
		
	# No returning answer, since I have to physically read the output.
	return None
