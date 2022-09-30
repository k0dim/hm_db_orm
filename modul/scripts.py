from os import getcwd, path
from json import load
from modul.models import Publisher, Shop, Book, Stock, Sale, create_tables, drop_tables
from tkinter import messagebox as mb 

# Загрузка JSON
def add_json(session):
    try:
        ROAD = getcwd()
        FILES = 'files'
        FILE = 'fixtures.json'
        FULL_ROAS = path.join(ROAD, FILES, FILE)
        with open(FULL_ROAS, 'r') as file_json:
            data = load(file_json)
        for record in data:
            model = {
            'publisher': Publisher, 'shop': Shop, 'book': Book, 'stock': Stock, 'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
            session.commit()
        mb.showinfo('Выполненно', 'Данные успешно импортированы в Базу Данных')
        
    except:
        mb.showerror('Ошибка', f'Возможно записть "{record}" уже существует в БД')
    finally:
        session.close
# add_json(session)

# Найти по ID
def get_publisher_id(session, num):
    q = session.query(Publisher).filter(Publisher.id == num)
    for s in q.all():
        mb.showinfo('Выполненно', f'''ID: {s.id}
        Имя: {s.name}''')
# get_publisher_id(session, num)

# Найти по Имени
def get_publisher_name(session, num):
    q = session.query(Publisher).filter(Publisher.name == num)
    for s in q.all():
        mb.showinfo('Выполненно', f'''ID: {s.id}
        Имя: {s.name}''')
# get_publisher_name(session, num)

# Создать БД
def create_tab(engine):
    create_tables(engine)
    mb.showinfo('Выполненно', 'Таблицы созданы')

# Дроп БД
def drop_tab(engine):
    drop_tables(engine)
    mb.showinfo('Выполненно', 'Таблицы удалены')