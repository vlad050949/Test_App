import pymysql
from flask import Flask, render_template, request, redirect, url_for

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             passwd='root',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route("/CreateDB", methods=['GET'])
def input_create_db():
    return render_template('input_data.html', text='Придумай название базы данных')


@app.route("/CreateDB", methods=['POST'])
def create_db():
    name = request.form['name']

    create_db_cuery = "CREATE DATABASE " + name
    try:
        cursor.execute(create_db_cuery)
        connection.commit()
        print("База данных создана")
    except Exception as e:
        print(e)
    return redirect(url_for('index'))


@app.route("/DeleteDB", methods=['GET'])
def input_delete_db():
    return render_template('input_data.html', text='Какую базу удалить?')


@app.route("/DeleteDB", methods=['POST'])
def delete_db():
    name = request.form['name']

    drop_db_cuery = "DROP DATABASE " + name
    try:
        cursor.execute(drop_db_cuery)
        connection.commit()
        print("База данных удалена")
    except Exception as e:
        print(e)

    return redirect(url_for('index'))


@app.route("/CreateTB", methods=['GET'])
def input_create_tb():
    return render_template('input_data3.html',
                           text1='Напишите название таблицы',
                           text2='Напишите название колонки',
                           text3='Напишите тип данных(например VARCHAR(20)) ')


@app.route("/CreateTB", methods=['POST'])
def create_tb():
    name = request.form['name']
    name_col = request.form['name_col']
    int_col = request.form['int_col']

    create_table_query = "CREATE TABLE " + name + "(" + name_col + " " + int_col + ")"
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица создана")
    except Exception as e:
        print(e)

    return redirect(url_for('index'))


@app.route("/DeleteTB", methods=['GET'])
def input_delete_tb():
    return render_template('input_data.html', text='Напишите название таблицы которую хотите удалить')


@app.route("/DeleteTB", methods=['POST'])
def delete_tb():
    name = request.form['name']

    drop_table_query = "DROP TABLE " + name
    try:
        cursor.execute(drop_table_query)

        print("Таблица была успешно удаленна")
    except Exception as e:
        print(e)

    return redirect(url_for('index'))


@app.route("/ChangeTB", methods=['GET'])
def change_tb():
    return render_template('input_change.html')


@app.route("/ChangeTB/Edit", methods=['GET'])
def input_edit_tb():
    return render_template('input_data3.html',
                           text1='Напишите название таблицы в которую вы хотите внести изменения ',
                           text2='Напишите название колонки куда вы хотите сделать запись ',
                           text3='Сделайте запись в колонку ')


@app.route("/ChangeTB/Edit", methods=['POST'])
def edit_tb():
    name = request.form['name']
    name_col = request.form['name_col']
    int_col = request.form['int_col']

    change_col_query = "INSERT INTO " + name + " (" + name_col + ") VALUES('" + int_col + "');"
    try:
        cursor.execute(change_col_query)

        print("Таблица была успешно изменена")
        print(change_col_query)
    except Exception as e:
        print(e)

    return redirect(url_for("index"))


@app.route("/ChangeTB/Add", methods=['GET'])
def input_add_col():
    return render_template('input_data3.html',
                           text1='Напишите название таблицы ',
                           text2='Напишите название нашей новой колонки ',
                           text3='Напишите тип данных. Например VARCHAR(20) ')


@app.route("/ChangeTB/Add", methods=['POST'])
def add_col():
    name = request.form['name']
    name_col = request.form['name_col']
    int_col = request.form['int_col']
    add_col_query = "ALTER TABLE " + name + " ADD COLUMN " + name_col + " " + int_col
    try:
        cursor.execute(add_col_query)
        connection.commit()
        print("Колонка успешно добавлена")
    except Exception as e:
        print(e)

    return redirect(url_for('index'))


@app.route("/SelectTB", methods=['GET'])
def select_tb():
    return render_template('input_select.html')


@app.route("/SelectTB/Select_all", methods=['GET'])
def input_select_all():
    return render_template('input_data.html', text='Напишите название таблицы')


@app.route("/SelectTB/Select_all", methods=['POST'])
def select_all():
    name = request.form['name']
    import_table_query = "SELECT * FROM " + name
    try:
        cursor.execute(import_table_query)
        connection.commit()
    except Exception as e:
        print(e)

    data = cursor.fetchall()
    return render_template('data.html', data=data)


@app.route("/SelectTB/count", methods=['GET'])
def input_count():
    return render_template('input_data.html', text='Напишите название таблицы')


@app.route("/SelectTB/count", methods=['POST'])
def count():
    name = request.form['name']
    import_table_query = "SELECT COUNT(*) FROM " + name
    try:
        cursor.execute(import_table_query)
        connection.commit()
        print("Данные успешно импортированны")
    except Exception as e:
        print(e)


    data = cursor.fetchall()
    return render_template('data1.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)