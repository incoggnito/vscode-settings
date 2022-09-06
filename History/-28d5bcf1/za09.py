import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3\ml_database.db")
df = pd.read_sql("SELECT * FROM measurement", conn)