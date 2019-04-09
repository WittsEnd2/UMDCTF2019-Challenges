from flask import Flask, request, jsonify, session, Response, render_template, url_for
from flask_cors import CORS, cross_origin
import hashlib
import random
import re
import mysql.connector
app = Flask(__name__)
app.secret_key = "UMDCTF-2019"
app.config['SESSION_COOKIE_HTTPONLY'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

config = {
    'user': 'root',
    'password': 'UMD_CTF_DB_PW',
    'host': 'db',
    'port': '3306',
    'database': "umdctf"
}


# def primaryFilter(value):

#     blacklist = set([";", "-"])
#     value = ''.join([c for c in value if c not in blacklist])

#     # insert_pattern = re.compile("insert", re.IGNORECASE)
#     # Add some more re.compile filtering here...
#     # value = insert_pattern.sub("", value)
#     # singleQuote_pattern = re.compile("'", re.IGNORECASE)
#     # doubleQuote_pattern = re.compile('"', re.IGNORECASE)
#     # value = singleQuote_pattern.sub("''", value)
#     # value = doubleQuote_pattern.sub('""', value)
#     or_pattern = re.compile(" or ", re.IGNORECASE)
#     value = or_pattern.sub("",value)

#     value = value[0:15]

#     return value

def primaryFilter(value):
    blacklist = set([";", "-"])
    value = ''.join([c for c in value if c not in blacklist])
    value = value[0:15]
    return value


def filter1(value):
    value = primaryFilter(value)
    or_pattern = re.compile(" or ", re.IGNORECASE)
    and_pattern = re.compile(" and ", re.IGNORECASE)
    select_pattern = re.compile(" select ", re.IGNORECASE)
    value = or_pattern.sub("", value)
    value = and_pattern.sub("", value)
    value = select_pattern.sub("", value)
    return value


def filter2(value):
    value = filter1(value)
    value = re.sub("\d+", "", value)
    return value


def userAgentFilter(value):
    pattern = re.compile("sqlmap")
    if (pattern.search(value)):
        return True
    return False


def authenticated():
    rv = []
    session_token = session['user']
    print(session['user'])
    # "admin", "71aaf9698acfcdeb382bac8de0406ea8e8561d60455af041", "umd")
    db = mysql.connector.connect(**config)
    # db = pymysql.connect(db_host, db_user, db_password, database)
    cur = db.cursor(prepared=True)

    query = """SELECT username FROM sessions WHERE session_token = %s"""
    cur.execute(query, (session_token,))

    u = [x for x in cur]

    try:
        cur.execute("SELECT * FROM users WHERE username = '" +
                    str(u[0][0]) + "';")
    except:
        return {}
    for row in cur.fetchall():
        rv.append(row)
    if len(rv) > 0:
        return rv[0][0]
    else:
        return {}


@app.route('/api/authenticate', methods=["POST", "OPTIONS"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def verify():
    if request.method == "OPTIONS":
        resp = Response()
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'

        return resp
    else:
        counter = 0
        if(userAgentFilter(request.headers.get('User-Agent'))):
            return -1
        else:
            rv = []
            username = request.form['username']
            password = request.form['password']
            if username == "" or password == "":
                return "Invalid parameters"
            else:
                # username = "test'User-- -"
                # password = "password;"

                # blacklist = set(["'", '"', "-", ";"])
                # username = ''.join([c for c in username if c not in blacklist])
                # password = ''.join([c for c in password if c not in blacklist])

                username = filter2(username)
                password = filter2(password)
                print("reaches")

                print(username, password)
                # db = pymysql.connect(db_host, db_user, db_password, database)
                db = mysql.connector.connect(**config)

                print("reaches")

                cur = db.cursor()

                cur.execute("SELECT * FROM users WHERE username = '" +
                            str(username) + "' AND password = '" + str(password) + "';")
                for row in cur.fetchall():
                    theHash = hashlib.sha256(
                        username.encode('utf-8')).hexdigest()

                    rv.append(row + (theHash, ))
                cur.close()
                # if len(rv) > 0:
                #     session_token = random.randint(0, 1000000)

                #     cur = db.cursor()
                #     cur.execute("INSERT INTO sessions (session_token, username) VALUES ('" + str(session_token) + "', '" + str(username) + "');")
                #     cur.close()
                #     session['user'] = session_token
                #     print(session['user'])
                json = jsonify(rv)
                json.headers['Access-Control-Allow-Credentials'] = 'true'
                json.headers['Access-Control-Allow-Headers'] = "Content-Type"
                return json


@app.route('/api/flag', methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def flags():
    is_authenticated = request.form['info']
    if (is_authenticated != None and is_authenticated != ""):

        is_authenticated = is_authenticated.split("=")[1].split(";")[0]
        print(is_authenticated)
        flagid = int(request.form['flagid'])
        if (flagid == 1):
            return "/static/img/carl.jpg"
        if (flagid == 2):
            return "/static/img/g0sh.png"
        if (flagid == 3):
            return "/static/img/flagship.jpg"
        if (flagid == 4):
            if (is_authenticated == hashlib.sha256("giveMe".encode('utf-8')).hexdigest()):
                print("test")

                return jsonify({"img": "/static/img/shell_black_website-2.png", "flg": "UMDCTF-{y0u_w0uldnt_d0wnl0ad_@_flag}"})
            else:
                print(is_authenticated)
                print(hashlib.sha256("giveMe".encode('utf-8')).hexdigest())
                return "-2"

    return "-1"


@app.route('/')
def index():
    return render_template('index.html')


app.run(host="0.0.0.0")
