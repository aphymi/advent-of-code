from copy import deepcopy
import re
import time

def preprocess_input(lines):
	groups = []
	g = ""
	for line in lines:
		if not line:
			continue
		elif line == "Immune System:":
			g = "m"
		elif line == "Infection:":
			g = "n"
		else:
			group = {"weak": [], "immu": [], "grp": g, "iden": len(groups)}
			group["num"], group["hp"], group["attd"], group["init"] = map(int, re.findall("\d+", line))
			group["attt"] = re.search(r"(\w+) damage", line).groups()[0]
			
			if "(" in line:
				strt, end = line.index("(")+1, line.index(")")
				attrs = line[strt:end].split("; ")
				for attr in attrs:
					if attr.startswith("weak"):
						for el in attr[8:].split(", "):
							group["weak"].append(el)
					else:
						for el in attr[10:].split(", "):
							group["immu"].append(el)
			
			groups.append(group)
	
	return groups


def eff_dam(group):
	return group["num"] * group["attd"]


def calc_damage(at, de):
	if at["attt"] in de["immu"]:
		return 0
	
	eff = eff_dam(at)
	if at["attt"] in de["weak"]:
		eff *= 2
	
	return eff

def step(groups):
	live_groups = [group for group in groups if group["num"] > 0]
	immune = []
	infect = []
	for group in live_groups:
		(immune if group["grp"] == "m" else infect).append(group)
	
	# Select targets.
	targets = {}
	for group in sorted(live_groups, reverse=True, key=lambda u: (eff_dam(u), u["init"])):
		enemies = infect if group["grp"] == "m" else immune
		enemies = [e for e in enemies if e["iden"] not in targets.values()]
		if not enemies:
			continue
		
		eta = max(enemies, key=lambda e: (calc_damage(group, e), eff_dam(e), e["init"]))
		if calc_damage(group, eta) == 0:
			continue
		targets[group["iden"]] = eta["iden"]
	
	cont = False
	# Attaaaaaaaaaaaaaaacccckkkk.
	targets = sorted(targets.items(), reverse=True, key=lambda t: groups[t[0]]["init"])
	for at, de in targets:
		at, de = groups[at], groups[de]
		if at["num"] <= 0:
			continue
		damage = calc_damage(at, de) // de["hp"]
		if damage > 0:
			cont = True
		de["num"] -= damage
	return cont
	

def sim(groups):
	# It's possible for the battle to come down to 2+ opposing groups that have immunities to each
	#   other's attack types, or if they just can't do a full unit's worth of damage.
	# In that case, when the battle has no possible resolution, stop.
	cont = True
	
	# While there are still groups alive from each side.
	while (any(group["grp"] == "m" and group["num"] > 0 for group in groups) and
		   any(group["grp"] == "n" and group["num"] > 0 for group in groups) and cont):
		cont = step(groups)
	
	return groups
	

def part1(groups):
	groups = deepcopy(groups)
	
	return sum(group["num"] for group in sim(groups) if group["num"] > 0)

def part2(groups):
	ogroups = groups
	boost = 0
	
	def add_boost(groups, boost):
		for g in groups:
			if g["grp"] == "m":
				g["attd"] += boost
	
	# While any infection is still alive after combat.
	while any(g["grp"] == "n" and g["num"] > 0 for g in groups):
		groups = deepcopy(ogroups)
		boost += 1
		add_boost(groups, boost)
		sim(groups)
	
	return sum(group["num"] for group in groups if group["num"] > 0)
