from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tkinter import messagebox as mb, Label, Entry, Tk, Button, Toplevel
from modul.scripts import add_json, get_publisher_id, get_publisher_name,\
                            create_tab, drop_tab#, test_conn


class Search_id(Toplevel): # Окно: Поиск по ID
    def __init__(self, parent, session):
        super().__init__(parent)
        self.session = session
        self.title("Найти по ID")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry('305x180+{}+{}'.format(w//2, h//2))
        self.label = Label(self, text="Укажите идентификатор:", font=("Arial Bold", 15))
        self.label.grid(column=0, row=1)
        self.entry = Entry(self, width=30)
        self.entry.grid(column=0, row=2)
        self.button_search = Button(self, text="Поиск", command=self.search, width=30)
        self.button_search.grid(column=0, row=3)

    def search(self):
        get_publisher_id(self.session, self.entry.get())


class Search_name(Toplevel): # Окно: Поиск по имени
    def __init__(self, parent, session):
        super().__init__(parent)
        self.session = session
        self.title("Найти по имени")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry('305x180+{}+{}'.format(w//2, h//2))
        self.label = Label(self, text="Укажите имя:", font=("Arial Bold", 15))
        self.label.grid(column=0, row=1)
        self.entry = Entry(self, width=30)
        self.entry.grid(column=0, row=2)
        self.button_search = Button(self, text="Поиск", command=self.search, width=30)
        self.button_search.grid(column=0, row=3)

    def search(self):
        get_publisher_name(self.session, self.entry.get())


class App(Toplevel): # Окно с выбором действий
    def __init__(self, parent, session, engine):
        super().__init__(parent)
        # Подключение к БД
        self.session = session
        self.engine = engine

        # Параметры окна
        self.title("Python и БД. ORM")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry('305x180+{}+{}'.format(w//2, h//2))
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        # Текст и кнопки первого слоя
        self.label = Label(self, text="Выберите действие:", font=("Arial Bold", 20))
        self.label.grid(column=1, row=0)
        self.button_search = Button(self, text="Создать БД", width=30, command=self.create_db)
        self.button_search.grid(column=1, row=1)
        self.button_json = Button(self, text="Импортировать данные из JSON", command=self.import_json, width=30)
        self.button_json.grid(column=1, row=2)
        self.button_search = Button(self, text="Поиск (ID)", command=self.new_win_search_id, width=30)
        self.button_search.grid(column=1, row=3)
        self.button_search = Button(self, text="Поиск (имя)", command=self.new_win_search_name, width=30)
        self.button_search.grid(column=1, row=4)
        self.button_search = Button(self, text="Дропнуть БД", width=30, command=self.drop_db)
        self.button_search.grid(column=1, row=5)

    def import_json(self):
        add_json(self.session)

    def new_win_search_id(self):
        nw_id = Search_id(self, session=self.session)
        nw_id.grab_set()

    def new_win_search_name(self):
        nw_name = Search_name(self, session=self.session)
        nw_name.grab_set()

    def create_db(self):
        create_tab(self.engine)

    def drop_db(self):
        drop_tab(self.engine)

    def confirm_delete(self):
            message = "Вы уверены, что хотите закрыть это окно?"
            if mb.askyesno(message=message, parent=self):
                self.session.close()
                self.destroy()


class Authorization(Tk):
    def __init__(self):
        super().__init__()
        # Параметры окна
        self.title("Python и БД. ORM")
        self.lbl = Label(self, text="Подключитесь к БД:", font=("Arial Bold", 20))
        self.lbl.grid(column=1, row=0)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry('470x250+{}+{}'.format(w//2, h//2))

        # Ввод параметров для подключения к БД
        self.dbms = self.entry('СУБД:',0,1,1,1)
        self.database = self.entry('Имя БД:',0,2,1,2)
        self.host = self.entry('Хост:',0,3,1,3)
        self.port = self.entry('Порт:',0,4,1,4)
        self.username = self.entry('Имя пользователя:',0,5,1,5)
        # self.password = self.entry('Укажите пароль пользователя:',0,3,1,3)

        # Пароль сормирован не через функцию entry() для скратия символов "*"
        lbl = Label(self, text='Пароль пользователя', font=("Arial Bold", 14))
        lbl.grid(column=0, row=6)
        self.password = Entry(self, width=20, show="*")
        self.password.grid(column=1, row=6)

        # Автоподстановка
        self.database.insert(0, '')
        self.port.insert(0, '5432')
        self.host.insert(0, 'localhost')
        self.password.insert(0, '')
        self.username.insert(0, '')
        self.dbms.insert(0, 'postgresql')

        # Кнопка 
        self.but = Button(self, text="Выполнить", command=self.click)
        self.but.grid(column=1, row=7)

    def entry(self, text, lbl_column, lbl_row, entry_column, entry_row,): # Поле ввода
        lbl = Label(self, text=text, font=("Arial Bold", 14))
        lbl.grid(column=lbl_column, row=lbl_row)
        entry = Entry(self, width=20)
        entry.grid(column=entry_column, row=entry_row)
        return entry

    def click(self): # Функция при нажатии кнопки
        dbms = auth.dbms.get()
        username = auth.username.get()
        password = auth.password.get()
        host = auth.host.get()
        port = auth.port.get()
        database = auth.database.get()
        DSM = f'{dbms}://{username}:{password}@{host}:{port}/{database}'
        engine = create_engine(DSM)
        Session = sessionmaker(bind=engine)
        session = Session()
        # test_conn(session)
        try:
            app = App(self, session, engine)
            app.grab_set()
        except:
            mb.showerror('Ошибка', '''Не удалось подключиться к БД
            Проверьте заполняемые поля''')

if __name__ == '__main__':
    auth = Authorization()
    auth.mainloop()
