import dataclasses
import heapq
from typing import Generator

from util.parse import *


parse_input = compose(
	lambda lines: (lines[:-2], lines[-1]),
	lambda parts: (
		[tuple(rule.split(" => ")) for rule in parts[0]],
		parts[1],
	),
)

ReactionRule = tuple[str, str]
Molecule = str
Input = tuple[list[ReactionRule], Molecule]

def get_molecule_products(
	start_molecule: Molecule,
	reaction_rules: list[ReactionRule],
) -> Generator[Molecule, None, None]:
	seen = set()

	for reactant, product in reaction_rules:
		for index in range(len(start_molecule)):
			relevant = start_molecule[index: index + len(reactant)]
			if relevant == reactant:
				new_molecule = "".join([
					start_molecule[:index],
					product,
					start_molecule[index + len(reactant):],
				])
				if new_molecule not in seen:
					yield new_molecule
					seen.add(new_molecule)

@dataclasses.dataclass(frozen=True)
class ReactionStep:
	molecule: Molecule
	steps: int

	def get_key(self):
		return [len(self.molecule), self.steps]

	def __lt__(self, other: "ReactionStep") -> bool:
		return self.get_key() < other.get_key()
	
	def __hash__(self):
		return hash(self.molecule) ^ self.steps

def part1(inp: Input) -> int:
	reaction_rules, target_molecule = inp

	product_count = 0
	for _product in get_molecule_products(target_molecule, reaction_rules):
		product_count += 1

	return product_count

def part2(inp) -> int:
	reaction_rules, target_molecule = inp

	reversed_rules = [
		(b, a) for a, b in reaction_rules
	]

	reversed_rules.sort(key=lambda rule: -len(rule[0]))

	start_reaction = ReactionStep(molecule=target_molecule, steps=0)
	queue = [start_reaction]
	seen = set([start_reaction])
	while len(queue) > 0:
		cur = heapq.heappop(queue)
		if cur.molecule == "e":
			return cur.steps
		
		for product in get_molecule_products(cur.molecule, reversed_rules):
			step = ReactionStep(product, cur.steps + 1)
			if step in seen:
				continue

			seen.add(step)
			heapq.heappush(queue, step)
	
	raise Exception("Couldn't find")
