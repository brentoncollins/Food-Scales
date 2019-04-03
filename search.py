# coding=utf-8
from tkinter import *
import csv
from itertools import islice
from PIL import ImageTk, Image
import os
import serial
import threading
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
csvfile_us = open('{}/food_custom.csv'.format(dir_path), 'r')

ser = serial.Serial('/dev/ttyUSB0', 9600) #/dev/ttyUSB0 # COM4
custom_fieldnames = (
						'food_name', 'amount', 'calories', 'total_fat', 'saturated_fat', 'polyunsaturated_fat',
						'monounsaturated_fat', 'cholesterol', 'sodium', 'potassium',
						'total_carbohydrate', 'dietary_fiber', 'protein', 'sugar', 'image')


total_grams = 0.0

data = []

current_food = {
				'amount': 0.0,
				'calories': 0.0,
				'total_fat': 0.0, 'saturated_fat': 0.0,
				'cholesterol': 0.0, 'sodium': 0.0,
				'total_carbohydrate': 0.0,
				'dietary_fiber': 0.0, 'protein': 0.0,
				'sugar': 0.0,'total_grams': 0.0}

for x in islice(csv.DictReader(csvfile_us, custom_fieldnames), 1, None):
	data.append(x)

class ThreadingExample(object):
	""" Threading example class
	The run() method will be started and it will run in the background
	until the application exits.
	"""

	def __init__(self, interval=1):
		""" Constructor
		:type interval: int
		:param interval: Check interval, in seconds
		"""
		self.interval = interval

		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True                            # Daemonize thread
		thread.start()                                  # Start the execution

	def run(self):
		""" Method that runs forever """
		while True:
			# Do something
			read_serial = ser.readline().decode("utf-8")

			try:
				app.scale_var.set(float(read_serial))
			except ValueError:
				print("Value error")
				continue



class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		bottom_left_frame = Frame(root, width=50, height=1000, pady=0)
		bottom_left_frame.grid(row=1, column=0, padx=0, pady=1, sticky="W")

		left_frame = Frame(root, width=450, height=1000, pady=0)
		left_frame.grid(row=0, column=0, padx=0, pady=1, sticky="E")



		right_frame = Frame(root, width=450, height=1000, pady=0)
		right_frame.grid(row=0, column=1, padx=0, pady=1, sticky="E",rowspan=2)
		self.temp_food_list = {}
		self.index = 0
		self.temp_weight = 0
		self.scale_var = StringVar()
		self.temp_scale_var = StringVar()
		self.search_var = StringVar()
		self.result_var = StringVar()
		self.get_food = StringVar()
		self.search_var.trace("w", self.update_list)
		self.scale_var.trace("w", self.update_results)
		self.temp_scale_var.set(0)

		# Left Frame

		scrollbar = Scrollbar(left_frame, width=50)
		self.lbox = Listbox(left_frame, width=24, height=12, font=('Calibri', 20), yscrollcommand=scrollbar.set)
		scrollbar.pack(side="right", fill="y", expand=False)
		scrollbar.config(command=self.lbox.yview)
		self.lbox.bind('<<ListboxSelect>>', lambda event: self.onselect(self))

		self.search_entry = Entry(bottom_left_frame, textvariable=self.get_food,width=12,font=('Calibri', 24))
		self.search_button = Button(bottom_left_frame, text="Search", height=3, width=18,command=lambda: self.add_food(self.get_food.get()))
		self.delete_food = Button(bottom_left_frame, text="Remove selection", height=3,width=18, command=lambda: self.remove_food())


		self.exit_button= Button(right_frame, text= "EXIT", command=lambda: root.destroy())


		# Right Frame
		self.scale_results = Label(right_frame, text="Scale (g)")
		self.food = Label(right_frame, text="Food",font=('Calibr bold', 12))
		self.food_entry = Entry(right_frame, width=17)
		self.protein = Label(right_frame, text="Protein (g)")
		self.protein_entry = Entry(right_frame, width=10)
		self.protein_entry_scale = Entry(right_frame, width=7)
		self.fat = Label(right_frame, text="Fat (g)")
		self.fat_entry = Entry(right_frame, width=10)
		self.fat_entry_scale = Entry(right_frame, width=7)
		self.carbohydrates = Label(right_frame, text="Carbohydrates (g)")
		self.carbohydrates_entry = Entry(right_frame, width=7)
		self.carbohydrates_entry_scale = Entry(right_frame, width=7)
		self.calories = Label(right_frame, text="Calories")
		self.calories_entry = Entry(right_frame, width=7)
		self.calories_entry_scale = Entry(right_frame, width=7)
		self.sugar = Label(right_frame, text="Sugar (g)")
		self.sugar_entry = Entry(right_frame, width=7)
		self.sugar_entry_scale = Entry(right_frame, width=7)
		self.fiber = Label(right_frame, text="Fiber (g)")
		self.fiber_entry = Entry(right_frame, width=7)
		self.fiber_entry_scale = Entry(right_frame, width=7)
		self.sodium = Label(right_frame, text="Sodium (Na) (mg)")
		self.sodium_entry = Entry(right_frame, width=7)
		self.sodium_entry_scale = Entry(right_frame, width=7)
		self.cholesterol = Label(right_frame, text="Cholesterol (mg)")
		self.cholesterol_entry = Entry(right_frame, width=7)
		self.cholesterol_entry_scale = Entry(right_frame, width=7)
		self.saturated_fat = Label(right_frame, text="Saturated Fat (g)")
		self.saturated_fat_entry = Entry(right_frame, width=7)
		self.saturated_fat_entry_scale = Entry(right_frame, width=7)
		self.amount_g = Label(right_frame, text="Per x (g)")



		self.manual_entry = Button(right_frame, text="Save Entry", command=lambda: self.manual_entry_funct(), width=20,
		                           height=3)
		self.add_food_button = Button(right_frame, text="Add Food", command=lambda: self.add_food_list(), width=20,
		                              height=3)
		self.tare_button = Button(right_frame, text="Tare", command=lambda: self.tare(), width=10,
		                              height=3)


		self.current_food_lbox = Listbox(right_frame, width=24, height=5)
		self.scale_reading = Entry(right_frame, textvariable=self.temp_scale_var, width=5, font=('Calibri', 30))
		self.amount_g_entry = Entry(right_frame, width=7)
		self.scale_reading_label = Label(right_frame, text="Scale (g)", font=('Calibri', 30))

		self.reset_food_button = Button(
			right_frame, text="Reset Food", command=lambda: self.reset_temp_food(),
			width=20, height=3)
		self.results = Label(right_frame,
		                     textvariable=self.result_var)  # Find spot for this will include error messages


		# Left Frame

		self.lbox.pack(side="left", anchor="n", fill="both", expand=True)
		self.delete_food.grid(row=1, column=0, padx=2, pady=1, sticky="W")
		self.search_entry.grid(row=2, column=1, padx=2, pady=1, sticky="E")
		self.search_button.grid(row=2, column=0, padx=2, pady=1, sticky="W")



		# Right Frame
		self.exit_button.grid(row=0, column=0, padx=0, pady=0, sticky="W")

		self.scale_results.grid(row=0, column=0, padx=2, pady=1, sticky="E")
		self.food.grid(row=0, column=2, padx=0, pady=1, sticky="W")
		self.food_entry.grid(row=0, column=2, padx=0, pady=1, sticky="E", columnspan = 2)


		self.protein.grid(row=1, column=2, padx=0, pady=0, sticky="W")
		self.protein_entry.grid(row=1, column=2, padx=0, pady=0, sticky="E")
		self.protein_entry_scale.grid(row=1, column=0, padx=2, pady=0, sticky="E")

		self.fat.grid(row=2, column=2, padx=2, pady=0, sticky="W")
		self.fat_entry.grid(row=2, column=2, padx=0, pady=0, sticky="E")
		self.fat_entry_scale.grid(row=2, column=0, padx=2, pady=0, sticky="E")

		self.carbohydrates.grid(row=3, column=2, padx=2, pady=0, sticky="W")
		self.carbohydrates_entry.grid(row=3, column=2, padx=0, pady=0, sticky="E")
		self.carbohydrates_entry_scale.grid(row=3, column=0, padx=2, pady=0, sticky="E")

		self.calories.grid(row=4, column=2, padx=2, pady=0, sticky="W")
		self.calories_entry.grid(row=4, column=2, padx=0, pady=0, sticky="E")
		self.calories_entry_scale.grid(row=4, column=0, padx=2, pady=0, sticky="E")

		self.sugar.grid(row=5, column=2, padx=2, pady=0, sticky="W")
		self.sugar_entry.grid(row=5, column=2, padx=0, pady=0, sticky="E")
		self.sugar_entry_scale.grid(row=5, column=0, padx=2, pady=0, sticky="E")

		self.fiber.grid(row=6, column=2, padx=2, pady=0, sticky="W")
		self.fiber_entry.grid(row=6, column=2, padx=0, pady=0, sticky="E")
		self.fiber_entry_scale.grid(row=6, column=0, padx=2, pady=0, sticky="E")

		self.sodium.grid(row=8, column=2, padx=2, pady=1, sticky="W")
		self.sodium_entry.grid(row=8, column=2, padx=0, pady=1, sticky="E")
		self.sodium_entry_scale.grid(row=8, column=0, padx=2, pady=1, sticky="E")

		self.cholesterol.grid(row=9, column=2, padx=2, pady=1, sticky="W")
		self.cholesterol_entry.grid(row=9, column=2, padx=0, pady=1, sticky="E")
		self.cholesterol_entry_scale.grid(row=9, column=0, padx=2, pady=1, sticky="E")

		self.saturated_fat.grid(row=10, column=2, padx=2, pady=1, sticky="W")
		self.saturated_fat_entry.grid(row=10, column=2, padx=0, pady=1, sticky="E")
		self.saturated_fat_entry_scale.grid(row=10, column=0, padx=2, pady=1, sticky="E")

		self.amount_g.grid(row=11, column=2, padx=0, pady=1, sticky="W")
		self.amount_g_entry.grid(row=11, column=2, padx=0, pady=1, sticky="E")

		self.add_food_button.grid(row=14, column=0, padx=2, pady=1)
		self.tare_button.grid(row=11, column=0, padx=0, pady=0,rowspan=3)
		self.manual_entry.grid(row=14, column=2, padx=2, pady=1)

		self.scale_reading.grid(row=15, column=2, padx=2, pady=0, sticky="SE")
		self.current_food_lbox.grid(row=15, column=0, padx=2, pady=1, sticky="W", columnspan=1)

		self.scale_reading_label.grid(row=16, column=2, padx=2, pady=0, rowspan=3, sticky="NE")
		self.reset_food_button.grid(row=16, column=0, padx=2, pady=1, sticky="W")

		self.results.grid(row=19, column=0,columnspan=3, padx=2, pady=1, sticky="S")


		self.update_list()

	def tare(self):

		self.temp_weight = self.scale_var.get()

		self.temp_scale_var.set(float(self.temp_scale_var.get()) - float(self.temp_weight))







	def reset_temp_food(self):
		self.current_food_lbox.delete(0, END)

		current_food['amount'] = 0.0
		current_food['calories'] = 0.0
		current_food['total_fat'] = 0.0
		current_food['saturated_fat'] = 0.0
		current_food['cholesterol'] = 0.0
		current_food['total_carbohydrate'] = 0.0
		current_food['dietary_fiber'] = 0.0
		current_food['sodium'] = 0.0
		current_food['protein'] = 0.0
		current_food['total_grams'] = 0.0
		current_food['sugar'] = 0.0

		self.temp_food_list = {}

		self.result_var.set("Food list cleared")

		self.update_results()


	def add_food_list(self):
		""""Add food to meal list"""
		if self.scale_reading.get() == "":
			self.result_var.set("No scale reading, no amount of food to add to list.")

			return

		add_food_info = {
								'amount': self.amount_g_entry.get(),
								'calories': self.calories_entry.get(),
								'total_fat': self.fat_entry.get(), 'saturated_fat': self.saturated_fat_entry.get(),
								'cholesterol': self.cholesterol_entry.get(), 'sodium': self.sodium_entry.get(),
								'total_carbohydrate': self.carbohydrates_entry.get(),
								'dietary_fiber': self.fiber_entry.get(), 'protein': self.protein_entry.get(),
								'sugar': self.sugar_entry.get(), 'total_grams':self.scale_reading.get()}

		# Some stuff to update lest with total amount of food, cant remember how it works...
		# Creates a temp food list and does some stuff....

		# Update the current food dict, if there is already that food in dict just add it to the total
		# this dict keeps a record of the total amount of food.

		for k, v in add_food_info.items():
			current_food[k] = current_food.get(k) + float(add_food_info.get(k))

		#
		if self.food_entry.get() in self.temp_food_list:
			self.temp_food_list[self.food_entry.get()] = \
				round(float(self.temp_food_list[self.food_entry.get()]) + float(self.scale_reading.get()), 2)
		else:
			self.temp_food_list[self.food_entry.get()] = round(float(self.scale_reading.get()), 2)

		self.current_food_lbox.delete(0, END)

		self.current_food_lbox.insert(END, "Total - {} (g)".format(current_food['total_grams']))

		for k, v in self.temp_food_list.items():
			self.current_food_lbox.insert(END, "{} - {} (g)".format(k, v))

		self.result_var.set("{} add to food list.".format(self.food_entry.get()))

		# Need to zero scale here when the results are added to the temporary food list.
		self.update_results()
		self.tare()

	def update_results(self, *args):

		self.temp_scale_var.set(round(float(self.scale_var.get()) - float(self.temp_weight),1))

		try:
			if self.amount_g_entry.get() == 0.0 or self.amount_g_entry.get() is None:
				self.result_var.set("The amount per gram is set to 0 this will not work.")
			else:
			#	print(root.winfo_reqheight()) # Optimal 532
			#	print(root.winfo_reqwidth()) # Optimal 698



				if self.scale_reading.get() == "":
					#self.result_var.set("No scale reading")
					return

				grams = self.amount_g_entry.get()

				self.protein_entry_scale.delete(0, END)
				self.protein_entry_scale.insert(
												0, round(current_food['protein']
												+ (float(self.protein_entry.get())/float(grams))
												* (float(self.temp_scale_var.get())), 2)
												)

				self.fat_entry_scale.delete(0, END)
				self.fat_entry_scale.insert(
											0, round(current_food['total_fat']
											+ (float(self.fat_entry.get())/float(grams))
											* (float(self.temp_scale_var.get())), 2)
											)

				self.carbohydrates_entry_scale.delete(0, END)
				self.carbohydrates_entry_scale.insert(0, round(current_food['total_carbohydrate']
														+ (float(self.carbohydrates_entry.get())/float(grams))
														* (float(self.temp_scale_var.get())), 2)
														)

				self.sugar_entry_scale.delete(0, END)
				self.sugar_entry_scale.insert(0, round(current_food['sugar']
												+ (float(self.protein_entry.get())/float(grams))
												* (float(self.temp_scale_var.get())), 2)
												)

				self.calories_entry_scale.delete(0, END)
				self.calories_entry_scale.insert(0, round(current_food['calories']
													+ (float(self.calories_entry.get())/float(grams))
													* (float(self.temp_scale_var.get())), 2)
													)

				self.fiber_entry_scale.delete(0, END)
				self.fiber_entry_scale.insert(0, round(current_food['dietary_fiber']
												+ (float(self.fiber_entry.get())/float(grams))
												* (float(self.temp_scale_var.get())), 2)
												)

				self.sodium_entry_scale.delete(0, END)
				self.sodium_entry_scale.insert(0, round(current_food['sodium']
												+ (float(self.sodium_entry.get())/float(grams))
												* (float(self.temp_scale_var.get())), 2)
												)

				self.cholesterol_entry_scale.delete(0, END)
				self.cholesterol_entry_scale.insert(0, round(current_food['cholesterol']
													+ (float(self.cholesterol_entry.get())/float(grams))
													* (float(self.temp_scale_var.get())), 2)
													)

				self.saturated_fat_entry_scale.delete(0, END)
				self.saturated_fat_entry_scale.insert(0, round(current_food['saturated_fat']
														+ (float(self.saturated_fat_entry.get())/float(grams))
														* (float(self.temp_scale_var.get())), 2)
														)
		except ValueError:
			self.result_var.set("Value error in trying to calculate nutrition value")


		except ZeroDivisionError:
			self.result_var.set("Please enter an amount per x grams in the food data, cant divide by 0")

	def manual_entry_funct(self):
		""""Get food data from manual entry points and check to see if there is a duplicate, update if it has
		new values"""
		manual_info = {
							'food_name': self.food_entry.get(),
							'amount':self.amount_g_entry.get(),
							'calories': self.calories_entry.get(),
							'total_fat': self.fat_entry.get(),
							'saturated_fat': self.saturated_fat_entry.get(),
							'polyunsaturated_fat': 0.0, 'monounsaturated_fat': 0.0,
							'cholesterol': self.cholesterol_entry.get(), 'sodium': self.sodium_entry.get(),
							'potassium': 0.0, 'total_carbohydrate': self.carbohydrates_entry.get(),
							'dietary_fiber': self.fiber_entry.get(), 'protein': self.protein_entry.get(),
							'sugar': self.sugar_entry.get(), 'image': None}
		z = 0

		new_value = False
		new_food = True

		# Check is there is a food name the same, if there is check to see if any of the values are different
		# If not do nothing, if so remove from list and update entry.
		for x in data:
			if x['food_name'] == self.food_entry.get():

					for k, v in x.items():
						try:
							if float(v) != float(manual_info.get(k)):
								self.result_var.set("New Value, Updated food values")
								new_value = True
								data.pop(z)
								break
						except ValueError:
							print(
								"Value Error while checking {} against {} (Converted to a float)".format(
									v, manual_info.get(k)))
							continue



			z = z + 1

			for x in data:
				for k,v in x.items():
					if k.lower() == self.food_entry.get().lower():
						new_food = False
						break




		# If there is a new value in one of the fields
		if new_value is False:
			self.result_var.set("No new values")
			return

		# If no data in the food name do noting
		if self.food_entry.get() is None:
			self.result_var.set("No Data")
			return
		try:
			if new_food is True or new_value is True:
				# Append new item to the food list
				data.append(manual_info)

				self.update_list()
				self.save_data()

		except(TypeError):
			self.result_var.set("Use only number for input")

	def remove_food(self):
		""""Remove a food from food item list box"""
		data.pop(self.index)
		self.update_list()
		self.save_data()

	def save_data(self):
		""""Save list of current foods to the csv file"""
		try:
			with open('food_custom.csv', 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=custom_fieldnames)
				writer.writeheader()
				for x in data:
				#	print(x)
					writer.writerow(x)
		except IOError:
			self.result_var.set("I/O error, have you got the file open?")

	def add_food(self, search_term):

		self.info = nutrition.search_nutrition(search_term)
		if int(self.info[0]['calories']) == 0.0:
			self.result_var.set("No results")

			return
		else:

			self.result_var.set("Results found")
		# data.append(self.info)
			self.update_info(self.info,0)

	def update_list(self, *args):
		""""Populate list box with updated items"""
		search_term = self.search_var.get()

		self.lbox.delete(0, END)

		for dct in data:
			if dct['food_name'].lower() == 'ï»¿':
				continue

			if search_term in dct['food_name'].lower().replace(","," "):
				self.lbox.insert(END, dct['food_name'])

	def update_info(self, food_data, key):
		""""Add the food data to the food entry points for viewing or saving later"""

	#	print(data[key])
		self.food_entry.delete(0, END)
		self.food_entry.insert(0, food_data[key]["food_name"])

		self.protein_entry.delete(0, END)
		self.protein_entry.insert(0, food_data[key]["protein"])

		self.fat_entry.delete(0, END)
		self.fat_entry.insert(0, food_data[key]["total_fat"])

		self.carbohydrates_entry.delete(0, END)
		self.carbohydrates_entry.insert(0, food_data[key]["total_carbohydrate"])

		self.sugar_entry.delete(0, END)
		self.sugar_entry.insert(0, food_data[key]["sugar"])

		self.calories_entry.delete(0, END)
		self.calories_entry.insert(0, food_data[key]["calories"])

		self.fiber_entry.delete(0, END)
		self.fiber_entry.insert(0, food_data[key]["dietary_fiber"])

		self.sodium_entry.delete(0, END)
		self.sodium_entry.insert(0, food_data[key]["sodium"])

		self.cholesterol_entry.delete(0, END)
		self.cholesterol_entry.insert(0, food_data[key]["cholesterol"])

		self.saturated_fat_entry.delete(0, END)
		self.saturated_fat_entry.insert(0, food_data[key]["saturated_fat"])

		self.amount_g_entry.delete(0, END)
		self.amount_g_entry.insert(0, food_data[key]["amount"])

		# self.update_image(data[key]["image"])

	# def update_image(self,image):
	#
	#
	# 	self.pilImage = Image.open(image)
	# 	self.food_image = ImageTk.PhotoImage(self.pilImage)
	# 	self.img_label.update()
	#
	# 	img2 = ImageTk.PhotoImage(Image.open(image))
	# 	self.img_label.configure(image=img2)
	# 	self.img_label.image = img2
	#
	# 	root.update_idletasks()
	# 	return

	def onselect(event, self):
			# Note here that Tkinter passes an event object to onselect()
			w = event.lbox
			self.index = int(w.curselection()[0])
			value = w.get(self.index)

			x = 0
			for dct in data:

				if value.lower() == dct['food_name'].lower():
					self.update_info(data, x)

					self.result_var.set('You selected item %d: "%s"' % (x, dct['food_name']))

				x = x + 1
			self.update_results()

def read_serial():



	app.scale_var.set(ser.readline())
	root.after(1000, read_serial)


root = Tk()
#root.attributes('-fullscreen', True)
root.title('Filter Listbox Test')

app = Application(master=root)
example = ThreadingExample()
print ('Starting mainloop()')
app.mainloop()







