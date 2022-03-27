import cx_Oracle
import pandas as pd
from flask import Flask,request
import json

pool = cx_Oracle.SessionPool('melih', 'melih123','localhost:1521/orcl', min=1, max=20, increment=1)

query = ("""select * from melih.user_information""")

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello World'

@app.route("/login", methods=['POST'])
def login():
    
    request_data = request.get_json()
    
    user_mail = request_data['email']
    password = request_data['password']
    
    try:
        print("usermail")
        print(user_mail)
        print("user_password")
        print(password)
        
        conn = pool.acquire()
        queryUser = query + """ where user_mail = '""" + user_mail + """'"""
        sqlResult = pd.read_sql(queryUser, con=conn)
        print(sqlResult)
        user_mail_db = sqlResult['USER_MAIL'].iloc[0]
        print("user_mail_db")
        print(user_mail_db)
        user_password_db = sqlResult['USER_PASSWORD'].iloc[0]
        print("user_password_db")
        print(user_password_db)
        if user_mail == user_mail_db and password == user_password_db:
            print("başarılı")
            return json.dumps('{"code": 1, "result": "Login Succeeded", "displayName":"'+str(user_mail)+'"}', ensure_ascii=False)
        else:
            return json.dumps('{"code": -1, "result": "Password Error"}', ensure_ascii=False)
    except Exception as e:
        print(str(e))
        return json.dumps('{"code": -1, "result": "Password Error"}', ensure_ascii=False)


@app.route("/register")
def signUp():

    
    try:
        
        user_mail = request.args.get("filter1")
        user_password = request.args.get("filter2")
        
        print("usermail")
        print(user_mail)
        print("user_password")
        print(user_password)
        
        conn = pool.acquire()
        queryUser = query + """ where user_mail = '""" + user_mail + """'"""
        sqlResultUser = pd.read_sql(queryUser, con=conn)
        sqlResultTable = pd.read_sql(query, con=conn)
        print("sqlResultUser")
        print(sqlResultUser)
        if (sqlResultUser.empty):
            print(sqlResultTable)
            maxId = sqlResultTable['USER_ID'].max()
            print(maxId)
            newId = maxId + 1
            cursor = conn.cursor()
            addUser = ("""INSERT INTO melih.user_information (user_id, user_mail, user_password) VALUES ("""+str(newId)+""", '"""+user_mail+"""','"""+user_password+"""')""")
            print(addUser)
            cursor.execute(addUser)
            conn.commit()
            print("Registration Successfull!!")
            return json.dumps('{"code": 1, "result": "Registration Successfull!!"}', ensure_ascii=False)
        else:
            print("This email is exist!!")
            return json.dumps('{"code": -1, "result": "This email is exist!!"}', ensure_ascii=False)
            
    except Exception as e:
        print(str(e))
        return json.dumps('{"code": -1, "result": "Error!"}', ensure_ascii=False)

app.run(debug=True)