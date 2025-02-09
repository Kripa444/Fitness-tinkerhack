from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            favorite_flavor TEXT NOT NULL,
            sugar TEXT NOT NULL,
            pressure TEXT NOT NULL,
            cholesterol TEXT NOT NULL
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upi_id TEXT NOT NULL,
            status TEXT NOT NULL
        )''')
        conn.commit()

init_db()  # Ensure database setup

# Home Page
@app.route("/")
def home():
    return render_template("think.html")

# Form to collect user data
@app.route("/form", methods=["GET", "POST"])
def user_form():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        favorite_flavor = request.form["favorite_flavor"]
        sugar = request.form.get("sugar", "No")
        pressure = request.form.get("pressure", "No")
        cholesterol = request.form.get("cholesterol", "No")

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, gender, favorite_flavor, sugar, pressure, cholesterol) VALUES (?, ?, ?, ?, ?, ?)",
                           (name, gender, favorite_flavor, sugar, pressure, cholesterol))
            conn.commit()

        return redirect(url_for("recommendations.html"))

    return render_template("recommendations.html")

# Fetch users (for API)
@app.route("/api/users", methods=["GET"])
def get_users():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return jsonify([dict(user) for user in users])

# Payment submission route
@app.route('/submit-payment', methods=['POST'])
def submit_payment():
    try:
        data = request.get_json()
        upi_id = data.get('upi_id')
        status = data.get('status')

        if not upi_id or not status:
            return jsonify({"error": "Missing upi_id or status"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO payments (upi_id, status) VALUES (?, ?)", (upi_id, status))
            conn.commit()

        return jsonify({"message": "Payment details saved successfully!"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    

# Workout Pages
@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/pay')
def pay():
    return render_template('pay.html')

@app.route('/arm')
def arm():
    return render_template('arm.html')

@app.route('/leg')
def leg():
    return render_template('leg.html')

@app.route('/chest')
def chest():
    return render_template('chest.html')

@app.route('/posture')
def posture():
    return render_template('posture.html')

@app.route('/all')
def all():
    return render_template('all.html')
@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/workouts')
def workouts():
    return render_template('workouts.html')

# Health-related pages
@app.route('/diet')
def diet():
    return render_template('diet.html')
@app.route('/mentalhealth')
def mentalhealth():
    return render_template('mentalhealth.html')

@app.route('/physical')
def physical():
    return render_template('physical.html')

# Payment confirmation page
@app.route('/paid')
def paid():
    return render_template('paid.html')
@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')
if __name__ == "__main__":
    app.run(debug=True)
