import dataclasses
import itertools
import math
from typing import Generator

from util.parse import *


@dataclasses.dataclass
class BuyableItem:
	cost: int
	damage: int
	armor: int

@dataclasses.dataclass
class EntityInfo:
	hp: int
	damage: int
	armor: int
	cost: int = 0

	def with_item(self, item: BuyableItem) -> "EntityInfo":
		new = EntityInfo(
			hp=self.hp,
			damage=self.damage + item.damage,
			armor=self.armor + item.armor,
		)
		new.cost = self.cost + item.cost
		return new

parse_input = compose(
	joined_line,
	lambda line: [line],
	get_ints,
	lambda lines: lines[0],
	lambda inp: EntityInfo(*inp),
)

weapons = [
	BuyableItem(*stats)
	for stats in [
		(8, 4, 0),
		(10, 5, 0),
		(25, 6, 0),
		(40, 7, 0),
		(74, 8, 0),
	]
]

armors = [
	BuyableItem(*stats)
	for stats in [
		(13, 0, 1),
		(31, 0, 2),
		(53, 0, 3),
		(75, 0, 4),
		(102, 0, 5),
	]
]

rings = [
	BuyableItem(*stats)
	for stats in [
		(25, 1, 0),
		(50, 2, 0),
		(100, 3, 0),
		(20, 0, 1),
		(40, 0, 2),
		(80, 0, 3),
	]
]

def get_damage(attacker: EntityInfo, defender: EntityInfo) -> int:
	return max(
		1,
		attacker.damage - defender.armor,
	)

def get_winner(e1: EntityInfo, e2: EntityInfo) -> EntityInfo:
	turns_to_e1_win = math.ceil(
		e2.hp / get_damage(e1, e2),
	)
	turns_to_e2_win = math.ceil(
		e1.hp / get_damage(e2, e1)
	)

	return e1 if turns_to_e1_win <= turns_to_e2_win else e2

LoadoutWithCost = tuple[EntityInfo, int]

def get_possible_loadouts(
	player: EntityInfo,
) -> Generator[EntityInfo, None, None]:
	for weapon in weapons:
		player_with_weapon = player.with_item(weapon)

		for armor in itertools.chain([None], armors):
			player_with_armor = (
				player_with_weapon
				if armor is None
				else player_with_weapon.with_item(armor)
			)

			ring_choices = itertools.chain(
				*[
					itertools.combinations(rings, r)
					for r in range(3)
				]
			)
			for ring_loadout in ring_choices:
				player_with_rings = player_with_armor
				for ring in ring_loadout:
					player_with_rings = player_with_rings.with_item(ring)
				
				yield player_with_rings

def part1(boss_loadout: EntityInfo) -> int:
	loadouts = get_possible_loadouts(EntityInfo(100, 0, 0))
	viable_loadouts = (
		player_loadout
		for player_loadout in loadouts
		if get_winner(player_loadout, boss_loadout) == player_loadout
	)

	cheapest_loadout = min(
		viable_loadouts,
		key=lambda loadout: loadout.cost,
	)

	return cheapest_loadout.cost

def part2(boss_loadout: EntityInfo) -> int:
	loadouts = get_possible_loadouts(EntityInfo(100, 0, 0))
	unviable_loadouts = (
		player_loadout
		for player_loadout in loadouts
		if get_winner(player_loadout, boss_loadout) == boss_loadout
	)

	worst_loadout = max(
		unviable_loadouts,
		key=lambda loadout: loadout.cost,
	)

	return worst_loadout.cost
