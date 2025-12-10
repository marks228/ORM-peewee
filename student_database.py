from peewee import *

# Создаем базу
db = SqliteDatabase('my_students.db')
db.connect()


# Таблица студентов
class Student(Model):
    name = CharField()
    age = IntegerField()
    city = CharField()

    class Meta:
        database = db


# Создаем таблицу
Student.create_table()

# Добавление студентов(если нету)
if Student.select().count() == 0:
    students = [
        ('Max', 24, 'Spb'),
        ('John', 15, 'Spb'),
        ('Andy', 45, 'Manhester'),
        ('Kate', 34, 'Spb')
    ]

    for name, age, city in students:
        Student.create(name=name, age=age, city=city)
    print("Студенты добавлены")

# 1. Все студенты
print("Все студенты:")
for s in Student.select():
    print(f"- {s.name}, {s.age} лет, {s.city}")

# 2. Старше 30 лет
print("\nСтарше 30 лет:")
for s in Student.select().where(Student.age > 30):
    print(f"- {s.name}")

# 3. Из Spb
print("\nИз Spb:")
for s in Student.select().where(Student.city == 'Spb'):
    print(f"- {s.name}")

print("\nГотово!")
db.close()