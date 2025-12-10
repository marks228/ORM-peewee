from peewee import *

# Создаем базу данных
db = SqliteDatabase('students_courses.db')

# Создаем три таблицы
class Student(Model):
    id = IntegerField()
    name = CharField()
    surname = CharField()
    age = IntegerField()
    city = CharField()

    class Meta:
        database = db


class Course(Model):
    id = IntegerField()
    name = CharField()
    time_start = CharField()
    time_end = CharField()

    class Meta:
        database = db


class StudentCourse(Model):
    student_id = IntegerField()
    course_id = IntegerField()

    class Meta:
        database = db


# Подключаемся
db.connect()

# Создаем таблицы
db.create_tables([Student, Course, StudentCourse])

# Добавляем данные
if Student.select().count() == 0:
    # Добавляем курсы
    Course.create(id=1, name='python', time_start='21.07.21', time_end='21.08.21')
    Course.create(id=2, name='java', time_start='13.07.21', time_end='16.08.21')

    # Добавляем студентов
    Student.create(id=1, name='Max', surname='Brooks', age=24, city='Spb')
    Student.create(id=2, name='John', surname='Stones', age=15, city='Spb')
    Student.create(id=3, name='Andy', surname='Wings', age=45, city='Manhester')
    Student.create(id=4, name='Kate', surname='Brooks', age=34, city='Spb')

    # Добавляем связи
    StudentCourse.create(student_id=1, course_id=1)  # Max → python
    StudentCourse.create(student_id=2, course_id=1)  # John → python
    StudentCourse.create(student_id=3, course_id=1)  # Andy → python
    StudentCourse.create(student_id=4, course_id=2)  # Kate → java

# Тестирование
print("=" * 50)
print("ТЕСТИРОВАНИЕ ЗАПРОСОВ ИЗ ЗАДАНИЯ")
print("=" * 50)

#  Все студенты старше 30 лет
print("\n1. Студенты старше 30 лет:")
students_over_30 = Student.select().where(Student.age > 30)
count1 = students_over_30.count()

for student in students_over_30:
    print(f"   {student.name} {student.surname}, {student.age} лет")

print(f"   Всего: {count1} студента")
assert count1 == 2, f"ОШИБКА: должно быть 2, а есть {count1}"

# Все студенты на курсе python
print("\n2. Студенты на курсе python:")
# Находим всех студентов с курсом python
python_students = []
for link in StudentCourse.select().where(StudentCourse.course_id == 1):
    student = Student.get(Student.id == link.student_id)
    python_students.append(student)

for student in python_students:
    print(f"   {student.name} {student.surname}")

print(f"   Всего: {len(python_students)} студентов")
assert len(python_students) == 3, f"ОШИБКА: должно быть 3, а есть {len(python_students)}"

# Студенты на python из Spb
print("\n3. Студенты на python из Spb:")
python_spb_students = []
for student in python_students:
    if student.city == 'Spb':
        python_spb_students.append(student)

for student in python_spb_students:
    print(f"   {student.name} {student.surname}")

print(f"   Всего: {len(python_spb_students)} студентов")
assert len(python_spb_students) == 2, f"ОШИБКА: должно быть 2, а есть {len(python_spb_students)}"

# Проверка всех данных
print("\n" + "=" * 50)
print("ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ")
print("=" * 50)

print(f"Всего студентов: {Student.select().count()}")
print(f"Всего курсов: {Course.select().count()}")
print(f"Всего записей о курсах студентов: {StudentCourse.select().count()}")

# Проверяем связи
print("\nКто на каких курсах:")
for link in StudentCourse.select():
    student = Student.get(Student.id == link.student_id)
    course = Course.get(Course.id == link.course_id)
    print(f"   {student.name} {student.surname} → {course.name}")

print("\n" + "=" * 50)
print("Успех!")
print("=" * 50)

# Конец
db.close()