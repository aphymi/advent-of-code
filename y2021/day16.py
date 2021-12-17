import collections
import math
from typing import Generator

from util import utils
from util.parse import *


parse_input = compose(
	single_line,
	lambda line: bin(int(line, 16))[2:],
	lambda bits: bits.zfill(8 * utils.ceildiv(len(bits), 8))
)

def read_literal_bytes(
	packets: str,
	start_index: int,
) -> Generator[tuple[str, int], None, None]:
	cur_index = start_index
	while True:
		next_index = cur_index + 5
		yield (packets[cur_index:next_index], next_index)
		cur_index = next_index

PacketInfo = collections.namedtuple(
	"PacketInfo",
	["value", "version_sum", "next_index"],
)

def read_packet(packets: str, start_index: int) -> PacketInfo:
	version = int(packets[start_index:start_index+3], 2)

	instruction_id = int(packets[start_index+3:start_index+6], 2)

	if instruction_id == 4: # literal
		parts = []
		for bits, next_index in read_literal_bytes(packets, start_index+6):
			parts.append(bits[1:])
			if bits[0] != "1":
				break
		
		return PacketInfo(int("".join(parts), 2), version, next_index)
	
	else:
		length_type_id = packets[start_index+6]
		cur_index = start_index + 7
		operands = []
		version_sum = 0

		if length_type_id == "0":
			total_subpacket_length = int(packets[cur_index:cur_index+15], 2)
			cur_index += 15
			subpacket_end_index = cur_index + total_subpacket_length

			while cur_index < subpacket_end_index:
				sp_value, sp_version_sum, next_index = read_packet(
					packets,
					cur_index
				)
				cur_index = next_index
				version_sum += sp_version_sum
				operands.append(sp_value)
		
		else:
			total_subpacket_count = int(packets[cur_index:cur_index+11], 2)
			cur_index += 11
			subpacket_count = 0

			while subpacket_count < total_subpacket_count:
				subpacket_count += 1
				sp_value, sp_version_sum, next_index = read_packet(
					packets,
					cur_index
				)
				cur_index = next_index
				version_sum += sp_version_sum
				operands.append(sp_value)

		value: int
		if instruction_id == 0:
			value = sum(operands)
		elif instruction_id == 1:
			value = math.prod(operands)
		elif instruction_id == 2:
			value = min(operands)
		elif instruction_id == 3:
			value = max(operands)
		elif instruction_id == 5:
			value = int(operands[0] > operands[1])
		elif instruction_id == 6:
			value = int(operands[0] < operands[1])
		elif instruction_id == 7:
			value = int(operands[0] == operands[1])
		
		return PacketInfo(
			value,
			version_sum + version,
			cur_index,
		)

def part1(packets: str) -> int:
	return read_packet(packets, 0).version_sum

def part2(packets: str) -> int:
	return read_packet(packets, 0).value
