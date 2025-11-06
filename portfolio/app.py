from flask import Flask, render_template, request, redirect, url_for, flash
import json
import csv
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # নিরাপত্তার জন্য বদলে নিও

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "projects.json"
CONTACT_STORE = BASE_DIR / "data" / "messages.csv"


def load_projects():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@app.route("/")
def home():
    projects = load_projects()[:3]  # হোমপেজে টপ ৩ দেখাই
    return render_template("index.html", projects=projects)


@app.route("/projects")
def projects():
    projects = load_projects()
    return render_template("projects.html", projects=projects)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("সব ঘর পূরণ করো", "error")
        else:
            CONTACT_STORE.parent.mkdir(parents=True, exist_ok=True)
            newfile = not CONTACT_STORE.exists()
            with open(CONTACT_STORE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if newfile:
                    writer.writerow(["name", "email", "message"])  # header
                writer.writerow([name, email, message])
            flash("তোমার মেসেজ পাওয়া গেছে!", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
