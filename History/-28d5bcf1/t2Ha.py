import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3\ml_database.db")
df1 = pd.read_sql("SELECT * FROM measurement", conn)

conn = sqlite3.connect(r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3\ml_database.db")
df2 = pd.read_sql("SELECT * FROM measurement", conn)