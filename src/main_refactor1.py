import pandas as pd
import sqlite3

from demand_analitic import DemandAnalitic

df = pd.read_csv('src/csv/converted_salary.csv')
df['year'] = df['published_at'].str[:4]
df = df.drop(columns=['published_at'])

key_words = ["python", "питон", "пайтон"]

demand = DemandAnalitic(df, key_words)

connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()
demand.move_to_sql(connection, 'myapp_demand')
print("Moved to SQL")

demand.save_graphs('myapp/static/graphs/demand/')
print("Graphs saved")
