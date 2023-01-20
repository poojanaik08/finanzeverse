import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta= Deta(DETA_KEY)

db= deta.Base("finanzeverse")

def insert_values(username, period, incomes, expenses, savings, savings_target):
    return db.put({"username": username, "periods": period, "incomes": incomes, "expenses": expenses, "savings": savings, "savings_target": savings_target})

def fetch_all_values():
    res = db.fetch()
    return res.items

def get_username(username):
    return db.get(username)

