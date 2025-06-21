import sqlite3
from config import *

work = [
    ("Учитель", "Терпеливый",),
    ("Учитель", "Люблю детей"),
    ("Учитель", "Заботливый"),
    ("Архитектор", "Креативный"),
    ("Архитектор", "Творческий"),
    ("Программист", "Логичный"),
    ("Программист", "Люблю игры"),
    ("Программист", "Технический"),
    ("Дизайнер", "Внимательный"),
    ("Дизайнер", "Эстетический"),             
]

teacher = '''👨🏫 Учитель
                Чем занимается:
                Преподает предметы, воспитывает и развивает учеников.
                Плюсы:
                ✓ Возможность влиять на будущее поколение
                ✓ Творческий подход к урокам
                ✓ Длинный отпуск летом
                Минусы:
                ✗ Высокая эмоциональная нагрузка
                ✗ Часто — низкие зарплаты
                Навыки:
                Педагогика, терпение, харизма'''

arhet = '''🏛️ Архитектор
Чем занимается:
Проектирует здания и пространства.
Особенности:
• Сочетает инженерию и искусство
• Отвечает за безопасность проектов
Плюсы:
✓ Реальные воплощенные проекты
✓ Престижная профессия
Минусы:
✗ Высокая ответственность
✗ Долгое обучение
Что учить:
AutoCAD, Revit, 3D Max'''

program = '''💻 Программист
Чем занимается:
Пишет код для сайтов, приложений, игр и ИИ.
Языки:
Python (для анализа данных), JavaScript (для сайтов), C++ (для игр)
Плюсы:
✓ Огромные зарплаты
✓ Можно работать из любой точки мира
Минусы:
✗ Нужно постоянно учиться
✗ Сидячая работа
Старт:
Изучите HTML/CSS, затем Python или JavaScript'''

desiner = ''''🎨 Дизайнер
Чем занимается:
Создает визуальные решения (логотипы, интерфейсы, интерьеры).
Специализации:
• Графический дизайн
• UX/UI-дизайн
• Промышленный дизайн
Плюсы:
✓ Возможность работать удаленно
✓ Высокий спрос на рынке
Минусы:
✗ Субъективная оценка работы
✗ Конкуренция
Инструменты:
Figma, Adobe Photoshop, Illustrator'''
class Work:
    def __init__(self, db):
        self.db = db

    def create_tables(self):
        conn = sqlite3.connect(self.db)
        with conn:
            conn.execute('''
            CREATE TABLE work (
                works TEXT,
                reki TEXT,
                desk TEXT
            )
        ''')
            conn.execute('''
            CREATE TABLE users(
                        id INTEGER,
                        reki_us TEXT
                        )
                    ''')
            conn.executemany('INSERT INTO work (works,reki) VALUES(?,?)', work)
            conn.commit()
        with conn:
                conn.execute('UPDATE work SET desk = ? WHERE works = "Учитель"', (teacher,))
                conn.execute('UPDATE work SET desk = ? WHERE works = "Архитектор"', (arhet,))
                conn.execute('UPDATE work SET desk = ? WHERE works = "Программист"', (program,))
                conn.execute('UPDATE work SET desk = ? WHERE works = "Дизайнер"', (desiner,))
                conn.commit()


    def registr(self, id, reki):
        conn = sqlite3.connect(self.db)
        with conn:
            conn.execute('INSERT INTO users (id, reki_us) VALUES(?,?)', (id, reki))
            conn.commit()

    def perebor(self):
        conn = sqlite3.connect(self.db)
        with conn:
            sql = conn.execute('SELECT reki FROM work').fetchall()
            conn.commit()
        return sql
    
    def recomend_work(self, user_id):
        conn = sqlite3.connect(self.db)
        with conn:
            sql = conn.execute('SELECT reki_us FROM users WHERE id = ?', (user_id,)).fetchall()
            res = ''
            sort = []
            for i in sql:
                res = conn.execute('SELECT works FROM work WHERE reki = ?', (i)).fetchall()
                for item in res:
                    if item not in sort:
                        sort.append(item)
                result = ", ".join(it[0] for it in sort)
            conn.commit()
        return result

    def podbor_raboti(self, id):
        conn= sqlite3.connect(self.db)
        with conn:
            res = []
            sql = conn.execute('SELECT reki_us FROM users WHERE id = ?', (id,)).fetchall()
            for i in sql:
                sql = conn.execute('SELECT works FROM work WHERE reki = ?', (i)).fetchall()
                res.append(sql)
                for item in res:
                    if item not in res:
                        res.append(item)
            conn.commit()
            res = [item[0] for item in res if item]
            res = list(set(res))
            return res
        
    def deskription(self, reki):
        conn = sqlite3.connect(self.db)
        with conn:
            sql = conn.execute('SELECT desk FROM work WHERE works = ?', (reki,)).fetchone()
            conn.commit()
            return sql
        
    def delete_user(self, user_id):
        conn = sqlite3.connect(self.db)
        with conn:
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()

if __name__ == '__main__':
    manager = Work(database)
    manager.create_tables()