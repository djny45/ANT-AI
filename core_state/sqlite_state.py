import sqlite3
import json


class SQLiteState:
    def __init__(self, path="ant_state.db"):
        self.path = path

    def initialize(self):
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS goals(id INTEGER PRIMARY KEY, objective TEXT, subtasks TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS executions(id INTEGER PRIMARY KEY, step TEXT, result TEXT)")

    def save_goal(self, objective, subtasks):
        with sqlite3.connect(self.path) as db:
            cur = db.execute("INSERT INTO goals(objective,subtasks) VALUES(?,?)", (objective, json.dumps(subtasks)))
            return cur.lastrowid

    def log_execution(self, step, result):
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO executions(step,result) VALUES(?,?)", (json.dumps(step), json.dumps(result)))
