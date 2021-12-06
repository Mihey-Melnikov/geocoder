from tkinter import *
from tkinter import messagebox, ttk
from request_parser import *
from Address import Address
import pyperclip
import os
import data_base
import preprocessor


ADDRESS_LIST = []
DATABASE_EXIST = False


class GeoGui:
    def __init__(self):
        self.db = self.get_db()
        global DATABASE_EXIST
        if self.db:
            DATABASE_EXIST = True
        else:
            DATABASE_EXIST = False

        self.window = Tk()
        self.window.title("Geocoder")
        width = 700
        height = 325
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(width=False, height=False)
        self.window.iconphoto(False, PhotoImage(file="data/icon.png"))

        tab_control = ttk.Notebook(self.window)
        finder = ttk.Frame(tab_control)
        database = ttk.Frame(tab_control)
        tab_control.add(finder, text="Поиск")
        tab_control.add(database, text="База данных")
        tab_control.pack(expand=1, fill='both')

        db_frame = Frame(master=database)
        db_frame.place(x=0, y=0, height=300, width=440)

        self.db_info_city_count_lbl = Label(master=db_frame, text="Всего городов: 0", font="Arial 14")
        self.db_info_city_count_lbl.place(x=270, y=60)

        self.db_info_city_count_lbl = Label(master=db_frame, text="Всего домов: 0", font="Arial 14")
        self.db_info_city_count_lbl.place(x=280, y=90)

        db_create_btn = Button(master=db_frame, text="Сформировать базу данных", command=self.create_db)
        db_create_btn.place(x=255, y=210)

        db_delete_btn = Button(master=db_frame, text="Удалить базу данных", command=self.delete_db)
        db_delete_btn.place(x=275, y=250)

        input_frame = Frame(master=finder)
        input_frame.place(x=0, y=0, height=300, width=440)

        lbl_input_addr = Label(master=input_frame, text="Введите адрес:", font="Arial 12")
        lbl_input_addr.place(x=9, y=0)

        lbl_input_addr_help = Label(master=input_frame, text="Например: Екатеринбург Тургенева 4", fg="gray")
        lbl_input_addr_help.place(x=9, y=43)

        self.lbl_output_addr = Label(master=input_frame, text="Возможные адреса, всего 0:", justify=RIGHT, font="Arial 12")
        self.lbl_output_addr.place(x=9, y=75)

        self.txt_input_addr = Entry(master=input_frame)
        self.txt_input_addr.place(x=11, y=25, width=425)
        self.txt_input_addr.bind("<Return>", lambda _: self.find())

        btn_input = Button(master=input_frame, text="Найти", command=self.find)
        btn_input.place(x=391, y=50)

        btn_get = Button(master=input_frame, text="Выбрать", command=self.select_addr)
        btn_get.place(x=352.5, y=268)

        btn_up = Button(master=input_frame, text="▲", command=self.select_up)
        btn_up.place(x=412, y=268)

        btn_down = Button(master=input_frame, text="▼", command=self.select_down)
        btn_down.place(x=330, y=268)

        self.txt_output_addr = Listbox(master=input_frame)
        self.txt_output_addr.place(x=10, y=100, width=425, height=165)
        self.txt_output_addr.bind("<Double-Button-1>", lambda _: self.select_addr())

        scrl_output_addr = Scrollbar(master=self.txt_output_addr, orient="vertical")
        scrl_output_addr.config(command=self.txt_output_addr.yview)
        scrl_output_addr.pack(side="right", fill="y")

        self.txt_output_addr.config(yscrollcommand=scrl_output_addr.set)

        import_all_btn = Button(master=input_frame, text="Скопировать всё", command=self.copy_all)
        import_all_btn.place(x=10, y=268)

        output_frame = LabelFrame(master=finder, text="Гео данные")
        output_frame.place(x=440, y=5, height=290, width=250)

        latitude_lbl = Label(master=output_frame, text="Широта:", justify=RIGHT, font="Arial 10")
        latitude_lbl.place(x=5, y=5)
        self.latitude_output = Entry(master=output_frame, state="readonly")
        self.latitude_output.place(x=60, y=5, width=180)

        longitude_lbl = Label(master=output_frame, text="Долгота:", justify=RIGHT, font="Arial 10")
        longitude_lbl.place(x=5, y=35)
        self.longitude_output = Entry(master=output_frame, state="readonly")
        self.longitude_output.place(x=60, y=35, width=180)

        city_lbl = Label(master=output_frame, text="Город:", justify=RIGHT, font="Arial 10")
        city_lbl.place(x=5, y=65)
        self.city_output = Entry(master=output_frame, state="readonly")
        self.city_output.place(x=60, y=65, width=180)

        street_lbl = Label(master=output_frame, text="Улица:", justify=RIGHT, font="Arial 10")
        street_lbl.place(x=5, y=95)
        self.street_output = Entry(master=output_frame, state="readonly")
        self.street_output.place(x=60, y=95, width=180)

        house_lbl = Label(master=output_frame, text="Дом:", justify=RIGHT, font="Arial 10")
        house_lbl.place(x=5, y=125)
        self.house_output = Entry(master=output_frame, state="readonly")
        self.house_output.place(x=60, y=125, width=180)

        postcode_lbl = Label(master=output_frame, text="Индекс:", justify=RIGHT, font="Arial 10")
        postcode_lbl.place(x=5, y=155)
        self.postcode_output = Entry(master=output_frame, state="readonly")
        self.postcode_output.place(x=60, y=155, width=180)

        import_one_btn = Button(master=output_frame, text="Скопировать", command=self.copy_one)
        import_one_btn.place(x=80, y=240)

    @staticmethod
    def show_error(err_text="err_text"):
        if not DATABASE_EXIST:
            messagebox.showerror("Базы данных не существует!",
                                 "Создайте базу данных:\nБаза данных>Сформировать базу данных")
        else:
            messagebox.showerror("Ошибка", err_text)

    @staticmethod
    def show_info(info_text="info_text"):
        if not DATABASE_EXIST:
            messagebox.showerror("Базы данных не существует!",
                                 "Создайте базу данных:\nБаза данных>Сформировать базу данных")
        else:
            messagebox.showinfo("Успешно", info_text)

    def create_db(self):
        # добавить поток
        self.db = data_base.DataBase()
        # _thread.start_new_thread(preprocessor.run, (data_base.DataBase(), "data/big_mgn.osm"))
        preprocessor.run(self.db, "data/big_mgn.osm")
        # добавить прогрес бар
        self.show_info("База данных создана")
        global DATABASE_EXIST
        DATABASE_EXIST = True

    def delete_db(self):
        if not self.db:
            self.db.delete_table_geo()
        os.remove("data/geodatabase.db")
        # добавить вы точно уверены?
        self.show_info("База данных удалена")
        global DATABASE_EXIST
        DATABASE_EXIST = False # не получается удалить...

    @staticmethod
    def get_db():
        if os.path.exists("data/geodatabase.db"):
            return data_base.DataBase()
        return None

    @staticmethod
    def find_addr(city, street, house):
        for addr in ADDRESS_LIST:
            if addr.city == city and addr.street == street and addr.house == house:
                return addr

    def select_addr(self):
        try:
            addr_str = self.txt_output_addr.get(self.txt_output_addr.curselection())
        except:
            self.show_error("Адрес не выбран!")
            return
        addr_lst = addr_str.split(", ")
        addr = self.find_addr(addr_lst[0], addr_lst[1], addr_lst[2])
        self.fill_geo_output(addr)

    def select_up(self):
        current_selection = self.txt_output_addr.curselection()
        if len(current_selection) == 0:
            current_selection = 0
        else:
            current_selection = current_selection[0]
        self.txt_output_addr.selection_clear(current_selection)
        if current_selection == 0:
            current_selection = self.txt_output_addr.size()
        self.txt_output_addr.select_set(current_selection - 1)

    def select_down(self):
        current_selection = self.txt_output_addr.curselection()
        if len(current_selection) == 0:
            self.txt_output_addr.select_set(0)
        else:
            current_selection = current_selection[0]
            if current_selection == self.txt_output_addr.size() - 1:
                self.txt_output_addr.select_set(0)
                self.txt_output_addr.selection_clear(current_selection)
            else:
                self.txt_output_addr.select_set(current_selection + 1)
                self.txt_output_addr.selection_clear(current_selection)


    def fill_geo_output(self, addr):
        self.insert_output_data(self.latitude_output, addr.lat)
        self.insert_output_data(self.longitude_output, addr.lon)
        self.insert_output_data(self.city_output, addr.city)
        self.insert_output_data(self.street_output, addr.street)
        self.insert_output_data(self.house_output, addr.house)
        if addr.postcode is None:
            self.insert_output_data(self.postcode_output, "нет")
        else:
            self.insert_output_data(self.postcode_output, addr.postcode)

    @staticmethod
    def insert_output_data(place, data):
        place.config(state="normal")
        place.delete(0, END)
        place.insert(0, data)
        place.config(state="readonly")

    def find(self):
        global ADDRESS_LIST
        self.txt_output_addr.delete(0, self.txt_output_addr.size())
        ADDRESS_LIST.clear()
        addr = self.txt_input_addr.get()
        if addr == "":
            self.show_error("Пустой ввод!")
            return
        try:
            city, street, house = parse_question(addr, self.db)
        except:
            self.show_error("Ошибка ввода!")
            return
        self.add_addr(self.db.get_rows_by(city, street, house))
        self.lbl_output_addr.config(text=f"Возможные адреса, всего {len(ADDRESS_LIST)}:")
        for addr in ADDRESS_LIST:
            self.txt_output_addr.insert(0, addr)

    def add_addr(self, addresses):
        if type(addresses) is str:
            self.show_error(addresses)
            return
        if len(addresses) == 0:
            self.show_error("Адрес не найден в базе данных")
            return
        for addr in addresses:
            ADDRESS_LIST.append(Address(id=addr[0], city=addr[3], street=addr[4], house=addr[5],
                                        postcode=addr[6], lat=addr[1], lon=addr[2]))

    def copy_one(self):
        city = self.city_output.get()
        if city == "":
            self.show_error("Данные не выбраны")
            return
        street = self.street_output.get()
        house = self.house_output.get()
        copy_addr = self.find_addr(city, street, house)
        pyperclip.copy(copy_addr.full_addr())
        self.show_info("Данные скопированы в буфер обмена")

    def copy_all(self):
        all_addr = self.txt_output_addr.get(0, self.txt_output_addr.size())
        if len(all_addr) == 0:
            self.show_error("Данные не выбраны")
            return
        all_copy_addr = []
        for addr in all_addr:
            addr_lst = addr.split(", ")
            loking_addr = self.find_addr(addr_lst[0], addr_lst[1], addr_lst[2])
            all_copy_addr.append(loking_addr.full_addr())
        pyperclip.copy("\n\n".join(all_copy_addr))
        self.show_info("Данные скопированы в буфер обмена")

    def show(self):
        self.window.mainloop()


# он сам должен к базе подключаться, мы не должны ничего передавать
# попровить препроцессинг, есть косяки с повторениями