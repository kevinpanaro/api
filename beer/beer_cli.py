from refill import pour_beer
from os.path import isfile, join, dirname, realpath
import os
import logging


class BeerCLI():

	def __init__(self):
		DIR_BEER = dirname(realpath(__file__))
		self.DIR_TAPS = join(DIR_BEER, 'taps')
		self.start_up()
		self.menu()

	def start_up(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Beer Command Line Interface")

	def menu(self):
		user_input = raw_input("  [s]earch\n  [u]pdate\n  [q]uit\n -> ").lower()
		if self.validate(user_input, 0):
			print("handling {}".format(user_input))
			if user_input == 'u':
				self.update_menus()
			elif user_input == 's':
				self.search_menus()
			elif user_input == "q":
				print("bye now.")
		else:
			print("Invalid selection")
			return self.menu()


	def validate(self, user_input, menu_type):
		def main_menu():
			return ['s', 'u', 'q']

		def search_menu():
			return ['l', 'q']

		options = {0: main_menu,
				   1: search_menu,}

		valid = options[menu_type]()

		if user_input in valid:
			return True
		else:
			return False

	def update_menus(self):
		print("This will take a while.")
		logLevel = logging.WARN
		FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
		logging.basicConfig(format=FORMAT,level=logLevel)
		# pour_beer()
		self.menu()

	def search_menus(self):
		user_input = raw_input("  [l]ook up\n  [q]uit\n  ->").lower()
		if self.validate(user_input, 1):
			if user_input == 'l':
				print('lookup')
			elif user_input == 'q':
				print('quit')

		# self.brewerys = [file for file in os.listdir(self.DIR_TAPS) if isfile(join(self.DIR_TAPS, file))]
		# for num, brewery in enumerate(self.brewerys, start=1):
		# 	brewery_name = brewery.split('.')[0].split('_').title()
		# 	brewery_name = " ".join(brewery_name).title()


		



def main():

	BeerCLI()

if __name__ == '__main__':
	main()