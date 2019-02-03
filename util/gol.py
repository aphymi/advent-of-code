from functools import lru_cache

class GameOfLife:
	def __init__(self, initial_state=None, x_size=None, y_size=None):
		if initial_state is None:
			if x_size is None or y_size is None:
				raise Exception("If a GoL does not have an initial state specified, it must specified dimensions.")
			
			self.x_size = x_size
			self.y_size = y_size
			self.state = [[0 for _ in range(x_size)]
						     for _ in range(y_size)]
		
		else:
			self.x_size = len(initial_state[0])
			self.y_size = len(initial_state)
			self.state = initial_state
			
		self.t = 0
		
		# cur_value should only ever change once per step for any given coordinate,
		#   so caching the value and clearing between steps should save a lot of computation.
		self.cur_value = lru_cache(self.x_size*self.y_size)(self.cur_value)
	
	def cur_value(self, x, y):
		if 0 <= x < self.x_size and 0 <= y < self.y_size:
			return self.state[y][x]
		
		else:
			return 0
	
	def new_value(self, x, y, cur):
		raise NotImplementedError
	
	def step(self):
		self.t += 1
		self.state = [[self.new_value(x, y, self.cur_value(x, y))
		               for x in range(self.x_size)]
		               for y in range(self.y_size)]
		
		self.cur_value.cache_clear()
	
	def stepWhile(self, condition):
		while condition(self):
			self.step()
	
	def stepN(self, n):
		for _ in range(n):
			self.step()
	
	def score(self):
		return sum(self.cur_value(x, y) for x in range(self.x_size) for y in range(self.y_size))
	
	def visualise(self):
		return "\n".join("".join("#" if self.cur_value(x, y) else "."
								 for x in range(self.x_size)) for y in range(self.y_size))
	
	# Return the values of the 4 adjacent cells (no corners).
	def adj4(self, x, y):
		return [self.cur_value(x+xm, y+ym)
				for xm, ym in ((-1, 0), (1, 0), (0, -1), (0, 1))]
	
	def adj8(self, x, y):
		return [self.cur_value(x+xm, y+ym)
			for xm in (-1, 0, 1) for ym in (-1, 0, 1)
			if (xm, ym) != (0, 0)]
