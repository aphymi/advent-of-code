def preprocess_input(lines):
	routes = []
	for line in lines:
		l1, rest = line.split(" to ")
		l2, dist = rest.split(" = ")
		routes.append((l1, l2, int(dist)))
	return routes

def part1(routes):
	def shortest_route_from(rts, start): # Greedy!
		s = 0
		while rts:
			l1, l2, d = max([(l1, l2, d) for l1, l2, d in rts if start in (l1, l2)], key=lambda r: r[2])
			s += d
			rts = [(l1, l2, d) for l1, l2, d in rts if start not in (l1, l2)]
			start = [l for l in (l1, l2) if l != start][0]
		
		return s
	
	return max([shortest_route_from(routes, strt) for strt in set([rt[0] for rt in routes] + [rt[1] for rt in routes])])

def part2(routes):
	def longest_route_from(rts, start): # Exponential!
		if not rts:
			return 0
		
		next_rts = [([l for l in (l1, l2) if l != start][0], d) for l1, l2, d in rts if start in (l1, l2)]
		
		return max([d + longest_route_from([(l1, l2, d_) for (l1, l2, d_) in rts if start not in (l1, l2)], l)
							for l, d in next_rts])
	
	return max([longest_route_from(routes, strt) for strt in set([rt[0] for rt in routes] + [rt[1] for rt in routes])])
