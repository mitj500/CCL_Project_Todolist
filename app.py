from flask import Flask, render_template, request, redirect, url_for,session,flash

import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
app.config['SECRET_KEY'] = 'afdglnalnheognohe'

# Establish a global database connection
mydb = mysql.connector.connect(
    host="database-1.c7g86aoqaeg1.us-east-1.rds.amazonaws.com",
    user="admin",
    port=3306,
    password="12345678",
    database="db_ccl"
)
cursor = mydb.cursor()

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        # If user is not in session, redirect to login
        return redirect(url_for('login'))
    
    userid = session['user_id']
    print(userid)
    
    if request.method == 'POST':
        content = request.form['content']
        importance = int(request.form['degree'])

        query = "INSERT INTO todos (user_id, todo_name, importance) VALUES (%s, %s, %s)"
        values = (userid, content, importance)
        cursor.execute(query, values)
        print("Values:", values)
        mydb.commit()

        return redirect(url_for('index'))

    query = "SELECT todo_name, importance FROM todos WHERE user_id = %s"
    value = (userid,)
    cursor.execute(query,value)
    todos1 = cursor.fetchall()
    # print(todos1)

    return render_template('home.html', todos=todos1, userid = userid)

@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':
        todo_id = request.form['todo_id']

        query = "DELETE FROM todos WHERE todo_name = %s"
        values = (todo_id,)
        cursor.execute(query, values)
        mydb.commit()

        return redirect(url_for('index'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Insert data into the database
        insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        insert_values = (username, email, password)
        
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        cursor.execute(query, values)
        user = cursor.fetchone()
        
        try:
            if user:
                flash("user already exists")
                return redirect(url_for('signin'))

            # Execute the insert query
            cursor.execute(insert_query, insert_values)
            mydb.commit()
            return redirect(url_for('login'))
            
              
        except Error as e:
            # Handle MySQL errors gracefully
            # You can log the error or provide feedback to the user
            print("Error inserting user:", e)
            return redirect(url_for('signin'))  # Redirect to signup page or handle the error appropriately

    return render_template("signin.html")

@app.route('/success')
def success():
    return 'Sign-in successful!'

@app.route('/about')
def about_page():
    if 'user' not in session:
        # If user is not in session, redirect to login
        return redirect(url_for('login'))
    
    userid = session['user_id']
    
    return render_template("about.html", userid = userid)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        user = cursor.fetchone()
        print(user)

        if user:
            session['user'] = True
            
            session['user_id'] = user[1]
            
            print(session['user_id'])
            
            return redirect('/')
        else:
            # If username and password do not match, you may want to show an error message
            flash("wrong username or password")
            return redirect(url_for('login'))

    # If request method is not POST, render the login form
    return render_template('login.html')

@app.route('/sign_in')
def sign_in():
    return render_template("signin.html")

@app.route('/logout',methods=['GET','POST'])
def logout():
    if 'user' in session:
        session.pop("user",None)
        return redirect(url_for('login'))

@app.route('/canva')
def canva():
    return render_template("canva.html")

if __name__ == "__main__":
    app.run(debug=True)
