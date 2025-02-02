import sqlite3
from flask import g
import db

def get_connection():
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def get_recipes():
    sql = """SELECT r.id, r.recipe_name, COUNT(c.id) total, MAX(c.sent_at) last
             FROM recipes r, comments c
             WHERE r.id = c.recipe_id
             GROUP BY r.id
             ORDER BY r.id DESC"""
    return db.query(sql)
