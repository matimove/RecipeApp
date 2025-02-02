import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import forum


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    recipes = forum.get_recipes()
    return render_template("index.html", recipes=recipes)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    try:
        password_hash = db.query(sql, [username])[0][1]
        user_id = db.query(sql, [username])[0][0]
    except:
        return "ERROR: Wrong username or password. Please try again."

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    
    return "ERROR: Wrong username or password. Please try again."

    
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    
    return "Tunnus luotu"

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/profile")
def profile():
    recipes = forum.get_users_recipes(session["user_id"])
    return render_template("profile.html", recipes=recipes)

@app.route("/new_recipe", methods=["POST"])
def new_recipe():
    title = request.form["title"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]
    recipe_id = forum.add_recipe(title, ingredients, instructions, user_id)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    title = request.form["title"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    recipe_id = request.form["recipe_id"]
    user_id = session["user_id"]
    recipe_id = forum.update_recipe(title, ingredients, instructions, recipe_id)
    return redirect("/recipe/" + str(recipe_id))


@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = forum.get_recipe(recipe_id)
    print(recipe)
    #comments = forum.get_comments(recipe_id)
    comments = []
    return render_template("recipe.html", recipe=recipe, comments=comments)

@app.route("/remove/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    recipe = forum.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("remove.html", recipe=recipe)
    
    if request.method == "POST":
        forum.remove_recipe(recipe_id)
        return redirect("/")
    
@app.route("/edit/<int:recipe_id>", methods=["GET"])
def edit_recipe(recipe_id):
    recipe = forum.get_recipe(recipe_id)
    return render_template("edit.html", recipe=recipe)

@app.route("/update/<int:recipe_id>", methods=["POST", "GET"])
def update(recipe_id):
    title = request.form["title"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    forum.update_recipe(recipe_id, title, ingredients, instructions)
    return redirect("/recipe/" + str(recipe_id))
