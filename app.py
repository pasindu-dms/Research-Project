from flask import Flask, render_template, url_for, request, redirect, flash, session

import mysql.connector
from flask_restful import Resource, Api, reqparse
import sys
import os
import json
import requests
import http.client

import re

connClientHttp = http.client.HTTPSConnection("www.auth0.com")
headers = { 'authorization': "Bearer {eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imk5WWZoTGJCQjZmYXVtXzRZdVhxTSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mZ3o2cWx5cDJmdnl1eGZzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJRa3gyaEtkVldBcXNMTWZuWm1MTEM1S2ZXeXVnZ3A4NkBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtZmd6NnFseXAyZnZ5dXhmcy51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTY2ODIwMzcyNywiZXhwIjoxNjY4MjkwMTI3LCJhenAiOiJRa3gyaEtkVldBcXNMTWZuWm1MTEM1S2ZXeXVnZ3A4NiIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgcmVhZDp1c2VyX2N1c3RvbV9ibG9ja3MgY3JlYXRlOnVzZXJfY3VzdG9tX2Jsb2NrcyBkZWxldGU6dXNlcl9jdXN0b21fYmxvY2tzIGNyZWF0ZTp1c2VyX3RpY2tldHMgcmVhZDpjbGllbnRzIHVwZGF0ZTpjbGllbnRzIGRlbGV0ZTpjbGllbnRzIGNyZWF0ZTpjbGllbnRzIHJlYWQ6Y2xpZW50X2tleXMgdXBkYXRlOmNsaWVudF9rZXlzIGRlbGV0ZTpjbGllbnRfa2V5cyBjcmVhdGU6Y2xpZW50X2tleXMgcmVhZDpjb25uZWN0aW9ucyB1cGRhdGU6Y29ubmVjdGlvbnMgZGVsZXRlOmNvbm5lY3Rpb25zIGNyZWF0ZTpjb25uZWN0aW9ucyByZWFkOnJlc291cmNlX3NlcnZlcnMgdXBkYXRlOnJlc291cmNlX3NlcnZlcnMgZGVsZXRlOnJlc291cmNlX3NlcnZlcnMgY3JlYXRlOnJlc291cmNlX3NlcnZlcnMgcmVhZDpkZXZpY2VfY3JlZGVudGlhbHMgdXBkYXRlOmRldmljZV9jcmVkZW50aWFscyBkZWxldGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGNyZWF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgcmVhZDpydWxlcyB1cGRhdGU6cnVsZXMgZGVsZXRlOnJ1bGVzIGNyZWF0ZTpydWxlcyByZWFkOnJ1bGVzX2NvbmZpZ3MgdXBkYXRlOnJ1bGVzX2NvbmZpZ3MgZGVsZXRlOnJ1bGVzX2NvbmZpZ3MgcmVhZDpob29rcyB1cGRhdGU6aG9va3MgZGVsZXRlOmhvb2tzIGNyZWF0ZTpob29rcyByZWFkOmFjdGlvbnMgdXBkYXRlOmFjdGlvbnMgZGVsZXRlOmFjdGlvbnMgY3JlYXRlOmFjdGlvbnMgcmVhZDplbWFpbF9wcm92aWRlciB1cGRhdGU6ZW1haWxfcHJvdmlkZXIgZGVsZXRlOmVtYWlsX3Byb3ZpZGVyIGNyZWF0ZTplbWFpbF9wcm92aWRlciBibGFja2xpc3Q6dG9rZW5zIHJlYWQ6c3RhdHMgcmVhZDppbnNpZ2h0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOmxvZ3NfdXNlcnMgcmVhZDpzaGllbGRzIGNyZWF0ZTpzaGllbGRzIHVwZGF0ZTpzaGllbGRzIGRlbGV0ZTpzaGllbGRzIHJlYWQ6YW5vbWFseV9ibG9ja3MgZGVsZXRlOmFub21hbHlfYmxvY2tzIHVwZGF0ZTp0cmlnZ2VycyByZWFkOnRyaWdnZXJzIHJlYWQ6Z3JhbnRzIGRlbGV0ZTpncmFudHMgcmVhZDpndWFyZGlhbl9mYWN0b3JzIHVwZGF0ZTpndWFyZGlhbl9mYWN0b3JzIHJlYWQ6Z3VhcmRpYW5fZW5yb2xsbWVudHMgZGVsZXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRzIGNyZWF0ZTpndWFyZGlhbl9lbnJvbGxtZW50X3RpY2tldHMgcmVhZDp1c2VyX2lkcF90b2tlbnMgY3JlYXRlOnBhc3N3b3Jkc19jaGVja2luZ19qb2IgZGVsZXRlOnBhc3N3b3Jkc19jaGVja2luZ19qb2IgcmVhZDpjdXN0b21fZG9tYWlucyBkZWxldGU6Y3VzdG9tX2RvbWFpbnMgY3JlYXRlOmN1c3RvbV9kb21haW5zIHVwZGF0ZTpjdXN0b21fZG9tYWlucyByZWFkOmVtYWlsX3RlbXBsYXRlcyBjcmVhdGU6ZW1haWxfdGVtcGxhdGVzIHVwZGF0ZTplbWFpbF90ZW1wbGF0ZXMgcmVhZDptZmFfcG9saWNpZXMgdXBkYXRlOm1mYV9wb2xpY2llcyByZWFkOnJvbGVzIGNyZWF0ZTpyb2xlcyBkZWxldGU6cm9sZXMgdXBkYXRlOnJvbGVzIHJlYWQ6cHJvbXB0cyB1cGRhdGU6cHJvbXB0cyByZWFkOmJyYW5kaW5nIHVwZGF0ZTpicmFuZGluZyBkZWxldGU6YnJhbmRpbmcgcmVhZDpsb2dfc3RyZWFtcyBjcmVhdGU6bG9nX3N0cmVhbXMgZGVsZXRlOmxvZ19zdHJlYW1zIHVwZGF0ZTpsb2dfc3RyZWFtcyBjcmVhdGU6c2lnbmluZ19rZXlzIHJlYWQ6c2lnbmluZ19rZXlzIHVwZGF0ZTpzaWduaW5nX2tleXMgcmVhZDpsaW1pdHMgdXBkYXRlOmxpbWl0cyBjcmVhdGU6cm9sZV9tZW1iZXJzIHJlYWQ6cm9sZV9tZW1iZXJzIGRlbGV0ZTpyb2xlX21lbWJlcnMgcmVhZDplbnRpdGxlbWVudHMgcmVhZDphdHRhY2tfcHJvdGVjdGlvbiB1cGRhdGU6YXR0YWNrX3Byb3RlY3Rpb24gcmVhZDpvcmdhbml6YXRpb25zIHVwZGF0ZTpvcmdhbml6YXRpb25zIGNyZWF0ZTpvcmdhbml6YXRpb25zIGRlbGV0ZTpvcmdhbml6YXRpb25zIGNyZWF0ZTpvcmdhbml6YXRpb25fbWVtYmVycyByZWFkOm9yZ2FuaXphdGlvbl9tZW1iZXJzIGRlbGV0ZTpvcmdhbml6YXRpb25fbWVtYmVycyBjcmVhdGU6b3JnYW5pemF0aW9uX2Nvbm5lY3Rpb25zIHJlYWQ6b3JnYW5pemF0aW9uX2Nvbm5lY3Rpb25zIHVwZGF0ZTpvcmdhbml6YXRpb25fY29ubmVjdGlvbnMgZGVsZXRlOm9yZ2FuaXphdGlvbl9jb25uZWN0aW9ucyBjcmVhdGU6b3JnYW5pemF0aW9uX21lbWJlcl9yb2xlcyByZWFkOm9yZ2FuaXphdGlvbl9tZW1iZXJfcm9sZXMgZGVsZXRlOm9yZ2FuaXphdGlvbl9tZW1iZXJfcm9sZXMgY3JlYXRlOm9yZ2FuaXphdGlvbl9pbnZpdGF0aW9ucyByZWFkOm9yZ2FuaXphdGlvbl9pbnZpdGF0aW9ucyBkZWxldGU6b3JnYW5pemF0aW9uX2ludml0YXRpb25zIHJlYWQ6b3JnYW5pemF0aW9uc19zdW1tYXJ5IGNyZWF0ZTphY3Rpb25zX2xvZ19zZXNzaW9ucyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.b4fh7_wy6zlH4CJPQgcqq6NdiLkKUW9vPEm_Rsxp2IGYJkjI-zV83LyYMrpcDPwxY-uIZK-XKR-8TUTaFXnYELwLlJ-78o9A_BopfjcIV-WyInZ9YSlBxXxRJyT-GI7nZCDoff4xTvoc4d8KN8EX6spb1lui464kilDMCaJ35gGwybJf-TgT43cGWm6ZmcziwulBYzVVmN7E3iutSLluBOq5VRaMX6FdH5HMhR-xfMWwyER2eXpzMhTk27Awt2ufsF4-08zWT-TQlsYJgU_4xmC4PprTzspVQBWc0ZV3eRo8o9R9EYZZfhF2gozz--ehqBi7DuTpa1ueSXXvOhKMuQ}" }

conn=mysql.connector.connect(host="localhost",user="root",password="",database="bespoketailor")
cursor=conn.cursor()

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/register_user',methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')

        if email:

            acc_key = "b30a990668618198961804a129d6a995"
            req = requests.get('http://apilayer.net/api/check?access_key=' + acc_key + '&email=' + email)
            response = req.json()
    
            disposable = response["disposable"]
            format_valid = response["format_valid"]
            score = response["score"]
            mx_found = response["mx_found"]

            if format_valid == False or  mx_found == False :
                print("validated")
                msg = 'Email does not exists !'
                return render_template('registration.html',msg=msg)

            else :
                
                sql1 = "SELECT * FROM user WHERE email = %s"
                email1 = (email,)
                cursor.execute(sql1, email1)
                account = cursor.fetchall()

                if account:

                    print("here")
                    msg = 'Email already taken !'
                    return render_template('registration.html',msg=msg)
                    
                else:
                    #cursor.execute("insert into customer (first_name,last_name,birthday,gender,email,password) values (%s,%s,%s,%s,%s,%s)")
                    sql = "insert into user (email,password) values (%s,%s)"
                    val = (email,password)

                    cursor.execute(sql, val)
                    user_id = cursor.lastrowid

                    conn.commit()           

                    #Test
                    print(cursor.rowcount, "record inserted to user.")

                    #sql2 = "SELECT id FROM user WHERE email = %s"
                    #email2 = (email,)
                    #rint(email)

                    #cursor.execute(sql2, email2)
                    #print("success")

                    #user = cursor.fetchall()

                    #print(user[0])
                    #if user:
                    #    user_id = user[0][0]

                    sql = "insert into customer (user_id, firstname, lastname, birthday, gender,address) values (%s,%s,%s,%s,%s,%s)"
                    val = (user_id,first_name,last_name,birthday,gender,address)

                    cursor.execute(sql, val)

                    conn.commit()

                    flash('Account created successfully!')
                    #Test
                    print(cursor.rowcount, "record inserted to customer.") 

            return render_template('signin.html')

@app.route('/signin',methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(email)
        print(password)

        sqlQuery = "SELECT * FROM user WHERE email = %s AND password = %s"
        sqlNeedful = (email, password,)

        cursor.execute(sqlQuery, sqlNeedful)
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['email'] = account[1]
            session['user_id'] = account[0]
            user_id = account[0]

            sqlQCustomer = "SELECT * FROM customer WHERE user_id = %s "
            idQ = (user_id,)
            cursor.execute(sqlQCustomer, idQ)
            cusAccount = cursor.fetchone()

            if cusAccount:
                session['name'] = cusAccount[2]
                return render_template('index.html')
        else:
            flash('Invalid email or password!')
            return render_template('signin.html')

@app.route('/login_form')
def login_form():
    return render_template('signin.html')

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('user_id', None)
   session.pop('name', None)
   return redirect(url_for('login_form'))

@app.route('/sign_up')
def sign_up(): 
    return render_template('registration.html')

@app.route('/admin_index')
def admin_index(): 
    return render_template('admin-index.html')

if __name__ == "__main__":
    app.run(debug=True)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
# Define a function for
# for validating an Email
def check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


@app.rout
for('bshi'))
        if type == "3":
            return redirect(url_for('bt'))
        if type == "4":
            return redirect(url_for('bsho'))
    elif gendertype == "ladies":
        if type == "1":
            return redirect(url_for('gf'))
        if type == "2":
            return redirect(url_for('gs'))
        if type == "3":
            return redirect(url_for('gts'))
        if type == "4":
            return redirect(url_for('gt'))
    return "invalid"
@app.route('/gs')
def gs(): 
    return render_template ('g-s.html')

@app.route('/gt')
def gt(): 
    return render_template ('g-t.html')

@app.route('/gts')
def gts(): 
    return render_template ('g-ts.html')

@app.route('/gf')
def gf(): 
    return render_template ('g-f.html')

#--------------------------------------------

@app.route('/bshi')
def bshi(): 
    return render_template ('b-shi.html')

@app.route('/bsho')
def bsho(): 
    return render_template ('b-sho.html')

@app.route('/bt')
def bt(): 
    return render_template ('b-t.html')

@app.route('/bts')
def bts(): 
    return render_template ('b-ts.html')

@app.route('/chatbot',methods=['POST'])
def chatbot():
    
    i=False
    validated = False

    if request.method == 'POST':
        
        form = request.form.get('text')

        if('%') in form:
            form = form.replace('%', '')
            
            if ("1") in form:
                replyNull = "The following types of cloth stitching services are available in your preferred category:\n 1. Tshirt\n 2. Shirt\n 3.Trouser\n 4.Shorts\n\n (Please choose the index)"
                return replyNull

            if ("2") in form:
                replyNull = "The following types of cloth stitching services are available in your preferred category:\n 1. Frock\n 2. Skirt\n 3.Tshirt\n 4.Top\n\n (Please choose the index)"
                return replyNull
            
            else:
                replyNull = "Your reply was unrecognizable! Please choose the category again\n\nWhat gender of clothing do you favor?  if you prefer gents category please press 1 or if ladies press 2"
                return replyNull
        elif '*' in form:
                form = form.replace('*', '')
                replyNull = "To continue with your order please continue with following link "+'\n'+"http://127.0.0.1:5000/dresstype?type=" + form + "&gendertype=ladies"
                return replyNull
        elif '^' in form:
                form = form.replace('^', '')
                replyNull = "To continue with your order please continue with following link "+'\n'+"http://127.0.0.1:5000/dresstype?type=" + form + "&gendertype=gents"
                return replyNull
        elif '#'  in form:

            form = form.replace('#', '')
            replyNull = "Hello "+form+ ", welcome! \nWhat gender of clothing do you favor? \nif you prefer gents category please press 1 or if ladies press 2"

            session['name'] = form

            return replyNull

        elif check(form):

                acc_key = "b30a990668618198961804a129d6a995"
                req = requests.get('http://apilayer.net/api/check?access_key=' + acc_key + '&email=' + form)
                response = req.json()
        
                disposable = response["disposable"]
                format_valid = response["format_valid"]
                score = response["score"]
                mx_found = response["mx_found"]

                if format_valid == True or  mx_found == True :
                    print("validated")
                    validated = True
                    urlUser = '/dev-fgz6qlyp2fvyuxfs.us.auth0.com/api/v2/users-by-email?email='+form 
                    connClientHttp.request("GET", urlUser , headers=headers)

                    session['email'] = form

                    res = connClientHttp.getresponse()
                    data = res.read()
                    replyNull = "Enter your name"
                    return replyNull

        cursor.execute("SELECT * FROM bot WHERE queries LIKE %s LIMIT 1", ("%" + form + "%",))
        cusAccount = cursor.fetchone()

        if session.get('email') is not None:
            form = session.get('name')
            replyNull = "Hello "+form+ ", welcome! \nWhat gender of clothing do you favor? \nif you prefer gents category please press 1 or if ladies press 2"
            return replyNull
        if cusAccount:
            print(cusAccount[2])
            return cusAccount[2]
        else:
            replyNull = "Could not recognize your input! Please enter your email again to continue!"
            return replyNull  


@app.route('/order_completion_user_bshi',methods=['GET', 'POST'])
def order_completion_user(): 
    if request.method == 'POST':
        Collar = request.form.get('Collar')
        Yoke = request.form.get('Yoke')
        LeftFrontPart = request.form.get('Left-Front-Part')
        RightFrontpart = request.form.get('Right-Front-part')
        Backpart = request.form.get('Back-part')
        Sleeve = request.form.get('Sleeve')
        Pocket = request.form.get('Pocket')
        Buttons = request.form.get('Buttons')
        Cuffs = request.form.get('Cuffs')
        BoxPlate = request.form.get('Box-Plate')
        BodyBackPoint = request.form.get('Body-Back-Point')


        Necktoshoulder = request.form.get('Neck-to-shoulder')
        Sleevelength = request.form.get('Sleeve-length')
        ArmHole = request.form.get('Arm-Hole')
        Shoulder = request.form.get('Shoulder')
        Chest = request.form.get('Chest')
        Hem = request.form.get('Hem')
        Shirtlength = request.form.get('Shirt-length')
        Sleevecuff = request.form.get('Sleeve-cuff')
        CuffCircumference = request.form.get('Cuff-Circumference')

        sql = "insert into user (email,password) values (%s,%s)"
        val = (email,password)

        cursor.execute(sql, val)
        user_id = cursor.lastrowid

        conn.commit()   


