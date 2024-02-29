from flask import Flask
from package import mariadb as DB

app = Flask(__name__)

@app.route("/init")
def init():
    conn = DB.connect("root", "demo", "192.168.1.184", "3306", "app")
    DB.init(conn)
    return "<p>DB init successful!</p>"

@app.route("/")
def hello():
    return "<p>Welcome!</p>"

@app.route("/api/v1/hi")
def hi():
    conn = DB.connect("root", "demo", "192.168.1.184", "3306", "app")
    DB.addCount(conn, "/api/v1/hi")
    num = DB.getCount(conn, "/api/v1/hi")
    return "<p>Hello, there are " + str(num) + " user visited! </p>";

@app.route("/data")
def show():
    conn = DB.connect("root", "demo", "192.168.1.184", "3306", "app")
    api, counter, rows = DB.getTables(conn)
    return "<p>Table contents: " + api + " : " + str(counter) + " in total " + str(rows) + " rows</p>";

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

application = app
