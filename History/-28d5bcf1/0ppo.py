import sqlite3
import pandas as pd
from vallendb import FileHandler

wkd = r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3"
f = FileHandler("*", wkd=wkd)
conn = sqlite3.connect("ml_database.db")
df = pd.read_sql("SELECT * FROM measurement", conn)