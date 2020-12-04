from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/submit-form", methods=["POST"])
def form_submit():
    sqlite_connection = sqlite3.connect("deployTestDatabase.db")
    insert_query = "INSERT INTO user(USER_NAME, USER_EMAIL, USER_PASSWORD) VALUES(?, ?, ?);"
    values = (request.form.get("user_name"), request.form.get(
        "user_email"), request.form.get("user_password"))
    sqlite_connection.execute(insert_query, values)
    sqlite_connection.commit()
    sqlite_connection.close()
    return redirect(url_for("show_all_users"))


@app.route("/Show-all-users")
def show_all_users():
    sqlite_connection = sqlite3.connect("deployTestDatabase.db")
    select_all_query = "SELECT * FROM user;"
    data_retreived = sqlite_connection.execute(select_all_query)
    user_data = {}
    all_users = []
    for i in data_retreived:
        user_data["user_name"] = i[1]
        user_data["user_email"] = i[2]
        all_users.append(user_data)
        user_data = {}
    sqlite_connection.close()

    return render_template("viewResult.html", all_users=all_users)


if __name__ == "__main__":
    app.run(debug=True)
