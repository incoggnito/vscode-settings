import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3\ml_database.db")
df1 = pd.read_sql("SELECT * FROM measurement", conn)
df1 = df1.sort_values(by="timestamp_sent_vam_data")
masterlen = len(df1)

conn = sqlite3.connect(r"C:\Users\ahofer\Desktop\SmartSAD\Durchlauf_9_05_auf_8_3\20_05_04-all_features_db_pre_learning.sql")
df2 = pd.read_sql("SELECT * FROM measurement", conn)

