import dataclasses
from typing import Callable, Optional

from util.parse import *
from y2015.day21 import EntityInfo, get_damage


parse_input = compose(
	joined_line,
	lambda line: [line],
	get_ints,
	lambda lines: lines[0],
	lambda inp: EntityInfo(inp[0], inp[1], 0),
)

@dataclasses.dataclass(kw_only=True)
class MageInfo(EntityInfo):
	mana: int

MaybeMagicFunction = Optional[Callable[[EntityInfo], EntityInfo]]

class MagicEffect:
	turns_left: int
	start_effect: Optional[Callable]

	def apply(self, target: EntityInfo) -> tuple[EntityInfo, "MagicEffect"]:
		pass

@dataclasses.dataclass
class MagicBattle:
	p1: MageInfo
	p2: EntityInfo
	effects_on_p1: list
	effects_on_p2: list

	mana_spent: int = 0

	def __lt__(self, other: "MagicBattle") -> bool:
		return self.mana_spent < other.mana_spent
	



def part1(inp) -> int:
	return 0

def part2(inp) -> int:
	return 0
