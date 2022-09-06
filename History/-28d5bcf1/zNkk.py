import sqlite3
import pandas as pd

conn = sqlite3.connect("20_05_04-all_features_db_pre_learning.db")
df = pd.read_sql(con=conn, sql="measurement")