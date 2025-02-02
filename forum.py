import db

def get_recipes():
    sql = """SELECT r.id, r.recipe_name
             FROM recipes r
             ORDER BY r.id DESC"""
    return db.query(sql)

def get_users_recipes(user_id):
    sql = """SELECT r.recipe_name
             FROM recipes r LEFT JOIN users u
             ON r.user_id = u.id
             WHERE r.user_id == ?"""
    return db.query(sql, [user_id])

def add_recipe(title, ingredients, instructions, user_id):
    sql = """INSERT  INTO recipes (recipe_name, ingredients, instructions, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, ingredients, instructions, user_id])
    recipe_id = db.last_insert_id()
    return recipe_id

def update_recipe(recipe_id, title, ingredients, instructions):
    sql = """UPDATE recipes SET recipe_name = ?, ingredients = ?, instructions = ? WHERE id = ?"""
    db.execute(sql, [title, ingredients, instructions, recipe_id])
    return None

def get_recipe(recipe_id):
    sql = "SELECT id, recipe_name, ingredients, instructions, user_id FROM recipes WHERE id = ?"
    return db.query(sql, [recipe_id])[0]

def show_recipe():
    sql = """SELECT r.id, r.recipe_name
             FROM recipes r
             ORDER BY r.id DESC"""
    return db.query(sql)

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])
    return None


