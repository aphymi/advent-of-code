from datetime import datetime
import re

def preprocess_input(lines):
	lines_re = re.compile(r"\[(?P<dt>[^\]]+)\] (?P<text>.+)")
	
	parsed_lines = []
	for line in lines:
		match = lines_re.match(line).groupdict()
		dt = datetime.strptime(match["dt"], "%Y-%m-%d %H:%M")
		if match["text"].startswith("Guard"):
			match["gid"] = int(re.search("(\d+)", match["text"]).groups()[0])
		parsed_lines.append((dt, match))
	
	parsed_lines.sort(key=lambda l: l[0])
	
	logs = {}
	last_sl_start = 0
	last_guard = 0
	for dt, match in parsed_lines:
		
		if "gid" in match:
			gid = match["gid"]
			if gid not in logs:
				logs[gid] = []
			last_guard = gid
		
		elif match["text"] == "falls asleep":
			last_sl_start = dt.minute
		
		elif match["text"] == "wakes up":
			logs[last_guard].append((last_sl_start, dt.minute))
	
	return logs

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
