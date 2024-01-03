# RESOURCES
from mlproj4_data import *

# MAIN CLASS
class MLProject4(object):
	def __init__(self, debug, alg):
		self.debug = debug
		self.shuffled_items = None
		self.group = {
				"items": [], "vals": [], "cats": [], 
				"d_vals": [], "d_cats": [], 
				"type": None, "ret": 0, "step": 0
		}
		self.balance = 400
		self.cost = 1
		self.keep = None
		self.max_ret = 0
		self.max_group = None
		self.algorithms = {
			"i":  self.algorith_input,
			"r":  self.algorith_random,
			"k":  self.algorithm_keep_all,
			"d":  self.algorithm_discard_all,
			"s1": self.algorithm_strategy1,
		}
		self.algorithm = self.algorithms[alg]
		self.returns = {
			'RF': 0,
			'SF': 0,
			'4K': 0,
			'FH': 0,
			'F':  0,
			'S':  0,
			'3K': 0,
			'2P': 0,
			'JoB':0,
		}

	def reset(self):
		#self.keep = input("Reset:")
		if self.keep in QUIT:
			return
		items = copy.deepcopy(ITEMS_KEYS)
		random.shuffle(items)
		self.shuffled_items = items[:10]
		self.group["items"] = self.shuffled_items[:5]
		self.group["items"].sort()
		self.group["vals"] = [ITEMS[x]["val"] for x in self.group["items"]]
		self.group["vals"].sort()
		self.group["cats"] = [ITEMS[x]["cat"] for x in self.group["items"]]
		self.group["cats"].sort()
		self.group["d_vals"] =  [x - self.group["vals"][i - 1] for i, x in enumerate(self.group["vals"])][1:]
		self.group["d_cats"] =  [x - self.group["cats"][i - 1] for i, x in enumerate(self.group["cats"])][1:]

		print("\nInitial Group", self.group["items"])

		self.balance -= self.cost

	def algorith_input(self):
		keep = input("Algorithm Random: Keep: ")
		if keep == "r":
			keep = self.algorith_random()
		elif keep == "s1":
			keep = self.algorithm_strategy1()
		return keep

	def algorith_random(self):
		print("Algorithm Random:")
		num_choices = random.choice(NUM_ITEMS)
		keep_list = random.sample(NUM_ITEMS, num_choices)
		keep_list_str = [str(x) for x in keep_list]
		keep = "".join(keep_list_str)
		return keep

	def algorithm_keep_all(self):
		keep = "a"
		return keep

	def algorithm_discard_all(self):
		keep = "n"
		return keep

	def algorithm_strategy1(self):
		print("Algorithm Strategy 1:")
		keep = ""
		# Check for Straight Flushes:
		if self.group["d_cats"] == FLUSH and \
			self.group["d_vals"] in (STRAIGHT, AL_STRAIGHT):
			keep = "12345"

		# Check for Quads
		if keep == "":
			if self.group["d_vals"] == [0,0,0]:
					keep = "12345"

		# Check for Full Houses:
		if keep == "":
			if self.group["d_vals"][:2]  == [0,0] and self.group["d_vals"][3] == 0:
				keep = "12345"
			elif self.group["d_vals"][0] == 0 and self.group["d_vals"][2:] == [0,0]:
				keep = "12345"

		# Check for Straights or Flushes
		if keep == "":
			if self.group["d_cats"] == FLUSH :
				keep = "12345"
			elif self.group["d_vals"] in (STRAIGHT, AL_STRAIGHT):
				keep = "12345"

		# Check for Trips
		if keep == "":
			if self.group["d_vals"][:2]  == [0,0]:
				keep = "123"
			if self.group["d_vals"][1:3] == [0,0]:
				keep = "234"
			if self.group["d_vals"][2:]  == [0,0]:
				keep = "345"
			
		# Check for Pairs
		if keep == "":
			for i,x  in enumerate(self.group["d_vals"]):
				if x == 0 and i < 4:
					if str(i+1) not in keep:
						keep += str(i+1)
					if str(i+2) not in keep:
						keep += str(i+2)

		if keep == "":
			# Check for 4 to a Flush
			if self.group["d_cats"][:3] == FOUR_TO_A_FLUSH:
				keep = "1234"
				
			elif self.group["d_cats"][1:] == FOUR_TO_A_FLUSH:
				keep = "2345"

			# Check for 4 to a Straight
			elif self.group["d_cats"][:3] == FOUR_TO_A_STRIGHT:
				keep = "1234"

			elif self.group["d_cats"][1:] in (FOUR_TO_A_STRIGHT, FOUR_TO_A_STRIGHT2):
				keep = "2345"

			# Check for 3 to a Straight Flush
			elif self.group["vals"][:3] in THREE_TO_RF and self.group["cats"][:2] == THREE_TO_A_FLUSH:
				keep = "123"
			elif self.group["vals"][1:4] in THREE_TO_RF and self.group["cats"][1:3] == THREE_TO_A_FLUSH: 
				keep = "234"
			elif self.group["vals"][2:] in THREE_TO_RF and self.group["cats"][2:] == THREE_TO_A_FLUSH:
				keep = "345"
			elif self.group["vals"][:2] == [2,3] and self.group["vals"][4] == 14 and \
				self.group["cats"][0] == self.group["cats"][1] and self.group["cats"][0] == self.group["cats"][2]:
				keep = "125"

			# Check for High Value Items
			else:
				num_items = 0
				for i, item in enumerate(self.group["items"]):
					if ITEMS[item]["val"] > 10:
						keep += str(i+1)
						num_items += 1
						if num_items > 1:
							break

		return keep


	def update(self):
		if self.keep in QUIT:
			return

		if self.debug:
			print("Step",self.group["step"],"Shuffled items", self.shuffled_items)

		self.keep = self.algorithm()
		if self.debug:
			print("Keep", self.keep)

		if self.keep in QUIT:
			return

		elif self.keep in ALL:
			self.keep = ALL_ITEMS

		elif self.keep in NONE:
			self.keep = NO_ITEMS
		
		next_item = 5

		for item in NUM_ITEMS:
			item_str = str(item)

			if item_str not in self.keep:
				self.group["items"][item-1] = self.shuffled_items[next_item]
				next_item += 1

		self.group["items"].sort()
		self.group["vals"] = [ITEMS[x]["val"] for x in self.group["items"]]
		self.group["vals"].sort()
		self.group["cats"] = [ITEMS[x]["cat"] for x in self.group["items"]]
		self.group["cats"].sort()
		self.group["d_vals"] =  [x - self.group["vals"][i - 1] for i, x in enumerate(self.group["vals"])][1:]
		self.group["d_cats"] =  [x - self.group["cats"][i - 1] for i, x in enumerate(self.group["cats"])][1:]

		print("Updated Group", self.group["items"])
		
		if self.debug:
			print("Values", self.group["vals"])
			print("Values Diffs", self.group["d_vals"])
			print("Categories", self.group["cats"])
			print("Categories Diffs", self.group["d_cats"])

	def evaluate(self):
		if self.keep in QUIT:
			return

		self.group["type"] = None
		self.group["ret"] = 0

		if   is_rf(self.group):
			self.group["type"] = "RF"
		elif is_sf(self.group):
			self.group["type"] = "SF"
		elif is_4k(self.group):
			self.group["type"] = "4K"
		elif is_fh(self.group):
			self.group["type"] = "FH"
		elif is_f(self.group):
			self.group["type"] = "F"
		elif is_s(self.group):
			self.group["type"] = "S"
		elif is_3k(self.group):
			self.group["type"] = "3K"
		elif is_2p(self.group):
			self.group["type"] = "2P"
		elif is_job(self.group):
			self.group["type"] = "JoB"

		if self.group["type"]  in RETURNS_KEYS:
			self.group["ret"] = RETURNS_JoB_9_6[self.group["type"]]
			self.returns[self.group["type"]] += 1

		self.balance += self.group["ret"]


		print("Status:", 
			"Step", self.group["step"],
			"Type", self.group["type"], 
			"Ret", self.group["ret"], 
			"Bal", self.balance)

		if self.group["ret"] > self.max_ret:
			self.max_group = copy.deepcopy(self.group)
			self.max_ret = self.group["ret"]

	def step(self):
		self.group["step"] += 1
		self.reset()
		self.update()
		self.evaluate()
		
	def run(self):
		while (self.keep not in QUIT) and (self.balance > self.cost):
			self.step()
		print("num_steps", self.group["step"], 
			"\nmax_group", self.max_group,
			"\nreturns", self.returns)

# MAIN FUNCTION
def main(debug, alg):
	p4 = MLProject4(debug, alg)
	p4.run()

# COMMAND-LINE EXECUTION
if __name__=="__main__":
	parser = argparse.ArgumentParser(
			prog='MLProject4',
			description='Machine Learning Project 4',
	)
	parser.add_argument("-d","--debug", action='store_true')
	parser.add_argument("-a","--alg", default = "i")
	args = parser.parse_args()
	os.system("clear")
	main(args.debug, args.alg)