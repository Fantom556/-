import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Хранение и инициализация объектов GUI
    def init_main(self):
        # Создаём панель инструментов (тулбар)
        # bg - фон
        # bd - границы
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        # Упаковка
        # side закрепляет вверху окна
        # fill растягивает по горизонтали (x)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        # Создание кнопки добавления (command - функция по нажатию,
                                    # bg - фон,
                                    # bd - границы,
                                    # compound - ориентация текста (tk.CENTER , tk.LEFT , tk.RIGHT , tk.TOP или tk.BOTTOM),
                                    # image - иконка кнопки)
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img,
                                    command=self.open_dialog)
        # Упаковка и выравнивание по левому краю
        btn_open_dialog.pack(side=tk.LEFT)

        # Добавление Treeview (columns - столбцы, 
                             # height - высота таблицы, 
                             # show='headings' - скрытие нулевой (пустой) колонки таблицы)
        self.tree = ttk.Treeview(self, columns=('ID', 'name',
        'tel', 'email', 'salary'), height=45, show='headings')

        # Добавление параметров колонкам (width - ширина, 
                                        # anchor - выравнивание текста в ячейке)
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Заработная плата')

        # Упаковка
        self.tree.pack(side=tk.LEFT)
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # Редактирование
        self.update_image = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0',
                                    bd=0, image=self.update_image,
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img, 
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                              image=self.search_img,
                              command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

    # Поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()]

    # Метод, отвечающий за вызов дочернего окна 1
    def open_dialog(self):
        Child()

    # Добавление данных
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Вывод данных в виджет таблицы
    def view_records(self):
        # Выбор информации из БД
        self.db.c.execute('''SELECT * FROM db''')
        # Удаление всего из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавление в виджет таблицы всей информации из БД
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Метод, отвечающий за вызов дочернего окна 2
    def open_update_dialog(self):
        Update()

    # Метод обновления
    def update_records(self, name, tel, email, salary):
        self.db.c.execute('''UPDATE db SET name = ?, tel = ?, email = ?, salary = ?
        WHERE ID = ?''', (name, tel, email, salary, 
        self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE id = ?''',
            (self.tree.set(selection_item, '#1'),))
        
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self):
        Search()

# Класс дочерних окон (Toplevel - окно верхнего уровня)
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # Заголовок окна
        self.title('Добавить')
        # Размер окна
        self.geometry('400x220')
        # Запрет на изменения размеров окна
        self.resizable(False, False)
        # Перехват всех событий, происходящих в приложении
        self.grab_set()
        # Захват фокуса
        self.focus_set()

        # Подписи
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text='Заработная плата')
        label_salary.place(x=50, y=140)

        # Добавление строки ввода (self.entry_<> = ttk.Entry(self))
        self.entry_name = ttk.Entry(self)
        # Изменение координат объектов (self.entry_<>.place(x = <>, y = <>))
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # Кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть',
                                      command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        
        # Кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        # Срабатывание по ЛКМ
        self.btn_ok.bind('<Button-1>', lambda event:
                        # При нажатии кнопки вызывается метод records, которому передаются значения из строк ввода
                        self.view.records(self.entry_name.get(),
                                          self.entry_email.get(),
                                          self.entry_tel.get(),
                                          self.entry_salary.get()))

# Класс обновления данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        # Создание кнопки редактирования
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind("<Button-1>", lambda event:
                      self.view.update_records(self.entry_name.get(),
                                               self.entry_email.get(),
                                               self.entry_tel.get(),
                                               self.entry_salary.get()))
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    # Метод, автоматически заполняющий формы старыми данными
    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE
        id = ?''',
    (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        # Запрет на изменения размеров окна
        self.resizable(False, False)

        # Создание формы
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btw_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btw_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# Класс БД (база данных)
class DB:
    def __init__(self):
        # Создание соединения с БД
        self.conn = sqlite3.connect('db.db')
        # Создание объекта класса cursor, используемого для взаимодействия с БД
        self.c = self.conn.cursor()
        # Выполнение запроса к БД
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS db (id INTEGER PRIMARY KEY,
            name TEXT, tel TEXT, email TEXT, salary TEXT)''')
        # Сохранение изменений БД
        self.conn.commit()

    # Метод добавления в БД
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO db (name, tel, email, salary) VALUES(?, ?, ?, ?)
                       ''', (name, tel, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    # Экземпляр класса DB
    db = DB()
    app = Main(root)
    app.pack() 
    # Заголовок окна
    root.title('Телефонная книга')
    # Размер окна
    root.geometry('820x440')
    # Запрет на изменения размеров окна
    root.resizable(False, False)
    root.mainloop()