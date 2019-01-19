from util.parse import *

def get_logs(lines):
	logs = {}
	last_sl_start = None
	last_guard = None
	for line in lines:
		brack = line.index("]")
		minute = int(line[brack-2:brack])
		text = line[brack+2:]
		
		if "#" in text:
			num = text.index("#")
			last_guard = int(text[num+1:text.index(" ", num)])
			if last_guard not in logs:
				logs[last_guard] = []
		
		elif text == "falls asleep":
			last_sl_start = minute
		
		elif text == "wakes up":
			logs[last_guard].append((last_sl_start, minute))
	
	return logs

parse_input = compose(get_logs, sorted)

def part1(logs):
	guard = max(logs.items(), key=lambda t: sum([b-a for a, b in t[1]]))[0]
	
	max_minute = max(range(0, 60), key=lambda m: sum([1 if a <= m < b else 0 for a, b in logs[guard]]))
	
	return guard * max_minute

def part2(logs):
	minutes = []
	for m in range(60):
		for g in logs:
			minutes.append((m, g, sum([1 if a <= m < b else 0 for a, b in logs[g]])))
	
	max_minute = max(minutes, key=lambda x: x[2])
	return max_minute[0] * max_minute[1]
