from flask import Flask,redirect,render_template,url_for,request,session
from flask import flash
from flask_mysqldb import MySQL
import re

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="flask_db"

mysql=MySQL(app)


app.secret_key="layton"

@app.route('/')
def home():
    return render_template("home.html")



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users ")
        result = cur.fetchall()
        existing_usernames = [row[0] for row in result]
        if username in existing_usernames:
            flash("Username is already taken try another one !!")
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif len(password) < 8:
            flash("password must be more than 8 characters!")
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif not re.search("[a-z]", password):
            flash("password must have small letters!")
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif not re.search("[A-Z]", password):
            flash("password must have capital letters!")
            return render_template('register.html', name=name, username=username, email=email,password=password)
        elif not re.search("[_@$]+", password):
          flash("Password must contain special characters!")
          return render_template('register.html', name=name, username=username, email=email, password=password)
        else:
            cur.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)",
                        (name, username, email, password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
       name=request.form['nm']
       password=request.form['password']

       cur=mysql.connection.cursor()
       cur.execute("SELECT *FROM users WHERE username=%s AND password=%s",(name,password))
       result=cur.fetchone()

       if result is not None:
          session['name']=name[0]
          flash("log in successfully !")
          return redirect(url_for('welcome'))

       elif "name[1]" in session:
            flash("you are already logged in!!")
            return redirect(url_for('welcome'))

       else:
           flash("Invalid username or password !!")
        
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if "name" in session:
        name=session['name']
        return render_template('welcome.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('name[0]',None)
    flash("You have been logged out !",'error')
    return redirect(url_for('login'))


    if __name__=="__main__":
        app.run(debug=True)


