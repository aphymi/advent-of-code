from typing import List

from util.parse import *


def most_common_state(bits: List[str]) -> str:
	if bits.count("0") > bits.count("1"):
		return 0
	
	return 1

def get_gamma(bit_sets: List[str]) -> str:
	gamma_bits = []
	for i in range(len(bit_sets[0])):
		latest_bit = most_common_state([bits[i] for bits in bit_sets])
		
		gamma_bits.append(str(latest_bit))
	
	return "".join(gamma_bits)

def get_epsilon(gamma: str) -> str:
	return "".join(str(int(not int(bit))) for bit in gamma)


def part1(bitstrings: List[str]) -> int:
	gamma_rate = get_gamma(bitstrings)
	epsilon_rate = get_epsilon(gamma_rate)

	return int(gamma_rate, 2) * int(epsilon_rate, 2)


def part2(bitstrings: List[str]) -> int:
	o2_candidates = bitstrings
	co2_candidates = bitstrings

	for bit_position in range(len(bitstrings[0])):
		if len(o2_candidates) > 1:
			o2_gamma = get_gamma(o2_candidates)
			o2_candidates = [
				bitstring
				for bitstring in o2_candidates
				if bitstring[bit_position] == o2_gamma[bit_position]
			]
		
		if len(co2_candidates) > 1:
			co2_epsilon = get_epsilon(get_gamma(co2_candidates))
			co2_candidates = [
				bitstring
				for bitstring in co2_candidates
				if bitstring[bit_position] == co2_epsilon[bit_position]
			]
	
	o2 = int(o2_candidates[0], 2)
	co2 = int(co2_candidates[0], 2)

	return o2*co2


