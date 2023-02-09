import pandas as pd
import sqlite3

from demand_analitic import DemandAnalitic
from geography_analitic import GeographyAnalitic

df = pd.read_csv('src/csv/converted_salary.csv')
df['year'] = df['published_at'].str[:4]
df = df.drop(columns=['published_at'])

key_words = ["python", "питон", "пайтон"]

demand = DemandAnalitic(df, key_words)
geo = GeographyAnalitic(df, key_words)

connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()
demand.move_to_sql(connection, 'myapp_demand')
geo.move_to_sql(connection, 'myapp_geography')
connection.close()
print("Moved to SQL")

demand.save_graphs('myapp/static/graphs/demand/')
geo.save_graphs('myapp/static/graphs/geography/')
print("Graphs saved")
