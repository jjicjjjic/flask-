from flask import Flask, session, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
import os


mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '0000'
app.config['MYSQL_DATABASE_DB'] = 'music'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


@app.route('/', methods=['GET','POST'])
def main():
    error = None

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT id FROM users WHERE id = %s AND pw = %s"
        value = (id, pw)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in data:
            data = row[0]

        if data:
            session['login_user'] = id
            return redirect(url_for('home'))
        else :
            error='invalid input data detected !'
    return render_template('LoginPage.html', error = error)
 
 
@app.route('/RegisterPage.html', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        id = request.form['regi_id']
        print('id:', id)
        pw = request.form['regi_pw']
        print('pw:', pw)
 
        conn = mysql.connect()
        cursor = conn.cursor()
 
        sql = "INSERT INTO users VALUES ('%s', '%s')" % (id, pw)
        cursor.execute(sql)
 
        data = cursor.fetchall()
 
        if not data:
            conn.commit()
            return redirect(url_for('main'))
        else:
            conn.rollback()
            return "Register Failed"
 
        cursor.close()
        conn.close()
    return render_template('RegisterPage.html', error=error)
 
@app.route('/MainPage.html', methods=['GET', 'POST'])
def home():
    error = None
    id = session['login_user']

    if request.method == 'POST':
        content = request.form['content']
        conn = mysql.connect()
        
        cursor = conn.cursor()
        sql = "INSERT INTO contents (id, content, times) VALUES ('%s', '%s', now())" %(id, content)
        cursor.execute(sql)
        new_data = cursor.fetchall()

        if not new_data:
            conn.commit()
            return redirect(url_for("home"))
        else:
            conn.rollback()
            return "Register Failed"
        
        cursor.close()
        conn.close()

    elif request.method == "GET":
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = " SELECT content, id, times, num FROM contents ORDER BY num desc"
        cursor.execute(sql)
        data = cursor.fetchall()

        data_list = []

        for obj in data:
            data_dict = {
                'con':obj[0],
                'writer':obj[1],
                'time':obj[2],
                'num':obj[3]
            }

            data_list.append(data_dict)
        cursor.close()
        conn.close()

        return render_template('MainPage.html', error = error, name = id, data_list=data_list)
    return render_template('MainPage.html', error=error, name= id)
 
if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8000)), debug=True, use_reloader=False)
