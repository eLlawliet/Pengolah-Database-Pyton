import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class AppPage(tk.Frame):

	def __init__(self, parent, App):
		self.app = App
		self.settings = App.settings
		self.current_Database = self.settings.Database[0]
		self.last_current_Database_index = 0
		self.update_mode = False
		self.Databases_index = []


		super().__init__(parent) # window.conteiner
		self.grid(row=0, column=0, sticky="nsew")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.create_left_frame()
		self.create_right_frame()
		self.config_left_right_frame()


	def create_left_frame(self):
		self.left_frame = tk.Frame(self, bg="pink")
		self.left_frame.grid(row=0, column=0, sticky="nsew")
		self.create_left_header()
		self.create_left_content()

	def create_right_frame(self):
		self.right_frame = tk.Frame(self, bg="white", width=2*self.settings.width//3)
		self.right_frame.grid(row=0, column=1, sticky="nsew")
		self.create_right_header()
		self.create_right_content()
		self.create_right_footer()

	def config_left_right_frame(self):
		self.grid_columnconfigure(0, weight=1) # 1/3
		self.grid_columnconfigure(1, weight=2) # 2/3
		self.grid_rowconfigure(0, weight=1)

	def create_left_header(self):
		frame_w = self.settings.width//3
		frame_h = self.settings.height//5
		self.left_header = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_header.pack()

		image = Image.open(self.settings.logo)
		i_w, i_h = image.size
		ratio = i_w/frame_w
		new_size = (int(i_w/ratio),int(i_h/ratio)) #(x,y)
		image = image.resize(new_size)
		self.logo = ImageTk.PhotoImage(image)

		self.label_logo = tk.Label(self.left_header, image=self.logo)
		self.label_logo.pack()

		self.searchbox_frame = tk.Frame(self.left_header, bg="white", width=frame_w, height=frame_h//8)
		self.searchbox_frame.pack(fill="x")

		self.entry_search_var = tk.StringVar()
		self.entry_search = tk.Entry(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), textvariable=self.entry_search_var)
		self.entry_search.grid(row=0, column=0)

		self.button_search = tk.Button(self.searchbox_frame, bg="white", fg="black", font=("Arial", 14), text="Find", command=self.clicked_search_btn)
		self.button_search.grid(row=0, column=1)

		self.searchbox_frame.grid_columnconfigure(0, weight=3) # 3/4
		self.searchbox_frame.grid_columnconfigure(1, weight=1) # 1/4

	def show_Databases_in_listbox(self):
		Databases = self.settings.Database

		for index in self.Databases_index:
			Database = Databases[index]
			for key, value in Database.items():
				product = f"{value['Product_name']}"
				self.Database_listBox.insert("end", product)

	def show_all_Databases_in_listbox(self):
		Databases = self.settings.Database

		self.Databases_index = []
		counter_index = 0
		for Database in Databases:
			self.Databases_index.append(counter_index)
			counter_index += 1

		self.show_Databases_in_listbox()

	def create_left_content(self):
		frame_w = self.settings.width//3
		frame_h = 4*self.settings.height//5

		self.left_content = tk.Frame(self.left_frame, width=frame_w, height=frame_h, bg="white")
		self.left_content.pack(fill="x")

		self.Database_listBox = tk.Listbox(self.left_content, bg="white", fg="black", font=("Arial", 12), height=frame_h)
		self.Database_listBox.pack(side="left", fill="both", expand=True)

		self.Databases_scroll = tk.Scrollbar(self.left_content)
		self.Databases_scroll.pack(side="right", fill="y")

		self.show_all_Databases_in_listbox()

		self.Database_listBox.configure(yscrollcommand=self.Databases_scroll.set)
		self.Databases_scroll.configure(command=self.Database_listBox.yview)

		self.Database_listBox.bind("<<ListboxSelect>>", self.clicked_item_in_Listbox)


	def clicked_item_in_Listbox(self, event):
		if not self.update_mode:
			selection = event.widget.curselection()
			try:
				index_item = selection[0]
			except IndexError:
				index_item = self.last_current_Database_index
			index = self.Databases_index[index_item]
			self.last_current_Database_index = index
			print(index_item,"=>",index)
			self.current_Database = self.settings.Database[index]
			for Item_id, info in self.current_Database.items(): #Item_id -> Key, info -> Value
				ID = Item_id
				product = info['Product_name']
				Stok = info['Stock']
				Harga_jual = info['Harga_jual']
				Harga_beli = info['Harga_beli']
			#print(Database)
			self.product_label.configure(text=product)
			self.table_info[0][1].configure(text=ID)
			self.table_info[1][1].configure(text=Stok)
			self.table_info[2][1].configure(text=Harga_jual)
			self.table_info[3][1].configure(text=Harga_beli)


	def create_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.right_header = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_header.pack()
		self.create_detail_right_header()

	def create_detail_right_header(self):
		frame_w = 2*self.settings.width//3
		frame_h = self.settings.height//5

		self.detail_header = tk.Frame(self.right_header, width=frame_w, height=frame_h, bg="white")
		self.detail_header.grid(row=0, column=0, sticky="nsew")

		data = list(self.current_Database.values())[0]
		product = f"{data['Product_name']}"
		self.virt_img = tk.PhotoImage(width=1, height=1)
		self.product_label = tk.Label(self.detail_header, text=product, font=("Arial", 30), width=frame_w, height=frame_h, image=self.virt_img, compound="c", bg="white")
		self.product_label.pack()

		self.right_header.grid_columnconfigure(0, weight=1)
		self.right_header.grid_rowconfigure(0, weight=1)

	def create_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.right_content = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_content.pack(expand=True)
		self.create_detail_right_content()


	def create_detail_right_content(self):
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_content.grid(row=0, column=0, sticky="nsew")

		for Item_id, info in self.current_Database.items():
			info = [
				['ID :', Item_id],
				['Stok :', info['Stock']],
				['Harga jual :', info['Harga_jual']],
				['Harga beli :', info['Harga_beli']]
			]

		self.table_info = []

		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				label = tk.Label(self.detail_content, text=info[row][column], font=("Arial", 12), bg="white")
				aRow.append(label)
				if column == 0:
					sticky = "e"
				else:
					sticky = "w"
				label.grid(row=row, column=column, sticky=sticky)
			self.table_info.append(aRow)



		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)


	def create_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.right_footer = tk.Frame(self.right_frame, width=frame_w, height=frame_h, bg="white")
		self.right_footer.pack()
		self.create_detail_right_footer()

	def create_detail_right_footer(self):
		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4

		self.detail_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Update', 'Delete', 'Add New']
		commands = [self.clicked_update_btn, self.clicked_delete_btn, self.clicked_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)

	def recreate_right_frame(self):
		self.detail_header.destroy()
		self.detail_update_content.destroy()
		self.detail_update_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()


	def recreate_right_frame_after_delete(self):
		self.detail_header.destroy()
		self.detail_content.destroy()
		self.detail_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()

	def recreate_right_frame_after_add_new(self):

		self.detail_header.destroy()
		self.detail_add_new_content.destroy()
		self.detail_add_new_footer.destroy()

		#RECREATE HEADER
		self.create_detail_right_header()

		#RECREATE CONTENT
		self.create_detail_right_content()

		#RECREATE FOOTER
		self.create_detail_right_footer()


	def clicked_update_btn(self):
		self.update_mode = True
		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_update_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_update_content.grid(row=0, column=0, sticky="nsew")

		for Item_id, info in self.current_Database.items():
			info = [
				['Nama produk :', info['Product_name']],
				['Jumlah Stok :', info['Stock']],
				['ID :', Item_id],
				['Harga jual :', info['Harga_jual']],
				['Harga beli :', info['Harga_beli']]
			]

		self.table_info = []
		self.entry_update_Database_vars = []
		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_update_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_update_content,font=("Arial", 12), bg="white", textvariable=entry_var)
					entry.insert(0, info[row][column])
					aRow.append(entry)
					self.entry_update_Database_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_update_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_update_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_Database_btn, self.clicked_cancel_Database_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_update_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)



	def clicked_delete_btn(self):
		self.update_mode = True

		confirmed = messagebox.askyesnocancel("Databaseapp Conrifmation", "Are you sure to delete this Database?")
		index = self.last_current_Database_index
		if confirmed:
			self.settings.Database.pop(index)
			self.settings.save_data_to_json()
			self.last_current_Database_index = 0
			self.current_Database = self.settings.Database[self.last_current_Database_index]

		self.recreate_right_frame_after_delete()
		self.Database_listBox.delete(0, 'end')
		self.show_Databases_in_listbox()

		self.update_mode = False

	def clicked_add_new_btn(self):
		self.update_mode = True

		frame_w = 2*self.settings.width//3
		frame_h = 3*(4*self.settings.height//5)//4 

		self.product_label.configure(text="Tambah Kontak Baru")
		self.detail_content.destroy()
		self.detail_footer.destroy()

		self.detail_add_new_content = tk.Frame(self.right_content, width=frame_w, height=frame_h, bg="white")
		self.detail_add_new_content.grid(row=0, column=0, sticky="nsew")

		info = [
			['Nama produk :', None],
			['Jumlah Stok :', None],
			['ID :', None],
			['Harga jual :', None],
			['Harga beli :', None]
		]

		self.table_info = []
		self.entry_update_Database_vars = []
		rows , columns = len(info), len(info[0])
		for row in range(rows):
			aRow = []
			for column in range(columns):
				if column == 0:
					label = tk.Label(self.detail_add_new_content, text=info[row][column], font=("Arial", 12), bg="white")
					sticky = "e"
					label.grid(row=row, column=column, sticky=sticky)
					aRow.append(label)
				else:
					entry_var = tk.StringVar()
					entry = tk.Entry(self.detail_add_new_content,font=("Arial", 12), bg="white", textvariable=entry_var)
					aRow.append(entry)
					self.entry_update_Database_vars.append(entry_var)
					entry.grid(row=row, column=column, sticky=sticky)
					sticky = "w"
			self.table_info.append(aRow)

		self.right_content.grid_columnconfigure(0, weight=1)
		self.right_content.grid_rowconfigure(0, weight=1)

		frame_w = 2*self.settings.width//3
		frame_h = (4*self.settings.height//5)//4 

		self.detail_add_new_footer = tk.Frame(self.right_footer, width=frame_w, height=frame_h, bg="white")
		self.detail_add_new_footer.grid(row=0, column=0, sticky="nsew")

		features = ['Save', 'Cancel']
		commands = [self.clicked_save_add_new_btn, self.clicked_cancel_add_new_btn]
		self.buttons_features = []
		for feature in features:
			button = tk.Button(self.detail_add_new_footer, text=feature, bg="white", fg="black", font=("Arial", 12, "bold"), bd=0, command=commands[features.index(feature)])
			button.grid(row=0, column=features.index(feature), sticky="nsew", padx=20, pady=(0, 10))
			self.buttons_features.append(button)

		self.right_footer.grid_columnconfigure(0, weight=1)
		self.right_footer.grid_rowconfigure(0, weight=1)



	def clicked_save_Database_btn(self):
		self.update_mode = False

		confirmed = messagebox.askyesnocancel("Databaseapp Conrifmation", "Are you sure to update this Database?")

		if confirmed:
			Product_name = self.entry_update_Database_vars[0].get()
			Stock = self.entry_update_Database_vars[1].get()
			ID = self.entry_update_Database_vars[2].get()
			Harga_jual = self.entry_update_Database_vars[3].get()
			Harga_beli = self.entry_update_Database_vars[4].get()
			self.settings.Database[self.last_current_Database_index] = {
				ID : {
					"Product_name" : Product_name,
					"Stock" : Stock,
					"Harga_jual" : Harga_jual,
					"Harga_beli" : Harga_beli
				}
			}
			self.settings.save_data_to_json()
			self.current_Database = self.settings.Database[self.last_current_Database_index]

		self.recreate_right_frame()
		self.Database_listBox.delete(0, 'end')
		self.show_all_Databases_in_listbox()

	def clicked_cancel_Database_btn(self):
		self.update_mode = False

		self.recreate_right_frame()

	def clicked_search_btn(self):
		item_search = self.entry_search_var.get()
		if item_search:
			Databases = self.settings.Database
			self.Databases_index = []
			counter_index = 0
			for Database in Databases:
				for Item_id, info in Database.items():
					if item_search in Item_id:
						self.Databases_index.append(counter_index)
					elif item_search in info['Product_name']:
						self.Databases_index.append(counter_index)
					elif item_search in info['Stock']:
						self.Databases_index.append(counter_index)
				counter_index += 1
			self.Database_listBox.delete(0, 'end')
			self.show_Databases_in_listbox()
		else:
			self.Database_listBox.delete(0, 'end')
			self.show_all_Databases_in_listbox()

	def clicked_save_add_new_btn(self):
		self.update_mode = False

		confirmed = messagebox.askyesnocancel("Databaseapp Conrifmation", "Are you sure to add this Database?")
		Product_name = self.entry_update_Database_vars[0].get()
		Stock = self.entry_update_Database_vars[1].get()
		ID = self.entry_update_Database_vars[2].get()
		Harga_jual = self.entry_update_Database_vars[3].get()
		Harga_beli = self.entry_update_Database_vars[4].get()

		if confirmed and ID and Product_name:
			new_Database = {
				ID : {
					"Product_name" : Product_name,
					"Stock" : Stock,
					"Harga_jual" : Harga_jual,
					"Harga_beli" : Harga_beli
				}
			}
			self.settings.Database.append(new_Database)
			self.settings.save_data_to_json()
			index = len(self.settings.Database) - 1
			self.last_current_Database_index = index
			self.current_Database = self.settings.Database[self.last_current_Database_index]
		else:
			info = messagebox.showinfo("Databaseapp Confirmation", "Nothing To Save.")

		self.recreate_right_frame_after_add_new()
		self.Database_listBox.delete(0, 'end')
		self.show_all_Databases_in_listbox()

	def clicked_cancel_add_new_btn(self):
		self.update_mode = False
		self.recreate_right_frame_after_add_new()
		self.Database_listBox.delete(0, 'end')
		self.show_all_Databases_in_listbox()



