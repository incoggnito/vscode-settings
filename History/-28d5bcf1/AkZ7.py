import sqlite3
import pandas as pd

conn = sqlite3.connect("ml_database.db")
df = pd.read_sql("* FROM measurement", conn)