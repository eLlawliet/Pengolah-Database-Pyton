from json import load, dump


class Settings:

	def __init__(self):

		#App Conf
		self.title = "Database"

		#Window Conf
		base = 75
		ratio =(16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]

		self.screen = f"{self.width}x{self.height}"


		#Img Conf
		self.logo = "img/logo.jpeg"


		#Dummy Data

		self.Database = None
		self.load_data_from_json()

	def login(self, username, password):
		if username == "username" and password == "password":
			return True
		else:
			return False

	def load_data_from_json(self):
		with open("data/Database.json", "r") as json_file:
			self.Database = load(json_file)

	def save_data_to_json(self):
		with open("data/Database.json", "w") as json_file:
			dump(self.Database, json_file)






