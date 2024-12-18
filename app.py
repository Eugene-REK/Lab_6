# Лабораторная работа №6
#
# Задание
# Реализуйте следующее Web приложение на фреймворке Flask
#
# 1) создайте базу данных на движке SQLite при помощи Python, состоящей из одной таблицы и заполните ее вашими данными (не менее 10 строк).
# Таблицу можете выбрать любой тематики, например какие подарки необходимо купить родным / коллегам на Новый Год.
# Указать ФИО, название подарка, стоимость и статус (куплен / не куплен)
# Проверьте наличие данных в вашей таблице написав SQL запрос через Python
# SELECT * FROM ваша_таблица
#
# 2) возьмите файл базы данных созданной в задании 1) и выведите содержимое таблицы в HTML форме,
# используя Flask фреймворк и вызов GET запроса через браузер
#
# Пример вывода таблицы
#
# -----------------------------------------------------------------------------
# |   ФИО             |   Подарок         |   Стоимость       |   Статус      |
# -----------------------------------------------------------------------------
# |   Иван Иванович   |   Санки           |   2000            |   куплен      |
# |   Ирина Сергеевна |   Цветы           |   3000            |   не куплен   |
# |   ..              |   ..              |   ..              |   ..          |
# -----------------------------------------------------------------------------

import sqlite3
import random
import os
from faker import Faker
from flask import Flask, render_template

fake = Faker("ru_RU")
app = Flask(__name__)
obj = ['Цветы', 'Ваза', 'Машина', 'Статуэтка', 'Календарь', 'Картина', 'Телефон']
Status = ['Куплен', 'Не куплен']

filename = "templates/index.html"
dir_name = os.path.dirname(filename)

os.makedirs(dir_name, exist_ok=True)

with open(filename, "w", encoding='UTF-8') as file:
    file.write('''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" vontent="width=device-vidth, initial-scale=1.0">
    <title>Новогодний список</title>
    <style>
   table {
       table-layout: auto;
       width: 50%;
       border: 1px solid green;
       margin: auto;
   }
   td {
       max-width: 100%;
       text-align: center;
       font-size: 12px;
   }
  </style>
</head>
<body>
    <div class="container">
        <table border="1">
            <thead>
                <tr>
                    <th>ФИО</th>
                    <th>Подарок</th>
                    <th>Стоимость</th>
                    <th>Статус</th>
            </thead>
            <tbody>
            {% for news in data %}
                <tr>
                    <td>{{ news[0] }}</td>
                    <td>{{ news[1] }}</td>
                    <td>{{ news[2] }}</td>
                    <td>{{ news[3] }}</td>
                </tr>
            {% endfor %}
            </tbody>

        </table>
    </div>
</body>
</html>
''')


@app.route('/')
@app.route('/index')
def index():
    connection = sqlite3.connect('datab.db', check_same_thread=False)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT count(*) FROM `NY`").fetchall()
    except Exception:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS NY (FIO TEXT NOT NULL, Podarok TEXT NOT NULL, Stoimost INTEGER NOT NULL, Status TEXT NOT NULL)")
    if 1 > cursor.execute("SELECT count(*) FROM `NY`").fetchall()[0][0] < 10:
        for i in range(1, 10):
            cursor.execute("INSERT INTO `NY` (`FIO`, `Podarok`, `Stoimost`, `Status`) VALUES (?, ?, ?, ?)",
                           (fake.name(), random.choice(obj), random.randint(1, 20) ** 2 * 1000, random.choice(Status),))
    connection.commit()
    data = cursor.execute("SELECT * FROM `NY`").fetchall()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
