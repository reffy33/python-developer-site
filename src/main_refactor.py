import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

def get_analitic(df, agg_func):
    return df.groupby("year").agg({"salary": agg_func})


def get_profession_df(df, key_words):
    first = True
    for word in key_words:
        if first:
            first = False
            mask = df["name"].str.contains(word)
        else:
            new_mask = df["name"].str.contains(word)
            mask = mask | new_mask

    return df.loc[mask]


class DemandAnalitic():
    def __init__(self, df, key_words, prefix="python") -> None:
        prof_df = get_profession_df(df, key_words)
        self.prefix = prefix

        self.med_salary = self.__med_salary__(df)
        self.med_salary_prof = self.__med_salary__(prof_df, prefix=True)
        
        self.vac_count = self.__vac_count__(df)
        self.vac_count_prof = self.__vac_count__(prof_df, prefix=True)

        self.joined = self.join_all()

    def __med_salary__(self, df, prefix=False):
        med_salary = get_analitic(df, "median")
        if prefix:
            new_name = f'med_salary_{self.prefix}'
        else:
            new_name = 'med_salary'
        return med_salary.rename(columns={'salary': new_name})

    def __vac_count__ (self, df, prefix=False):
        vac_count = get_analitic(df, "count")
        if prefix:
            new_name = f'vac_count_{self.prefix}'
        else:
            new_name = 'vac_count'
        return vac_count.rename(columns={"salary": new_name})

    
    def __rename_to_rus__(self, df, dict):
        df.index.rename('Год', inplace=True)
        return df.rename(columns=dict)

    
    def rename_all(self):
        self.med_salary = self.__rename_to_rus__(self.med_salary, {'med_salary': "Медианная зарплата"})
        self.med_salary_prof = self.__rename_to_rus__(self.med_salary_prof, {f'med_salary_{self.prefix}': 'Медианная зарплата'})

        self.vac_count = self.__rename_to_rus__(self.vac_count, {'vac_count': "Количество вакансий"})
        self.vac_count_prof = self.__rename_to_rus__(self.vac_count_prof, {f'vac_count_{self.prefix}': "Количество вакансий"})


    def save_graphs(self, path, traslate=True):
        if traslate:
            self.rename_all()
        
        self.save_graph(self.med_salary, path + 'year_analitic_salary.png')
        self.save_graph(self.vac_count, path + 'year_analitic_count.png')

        self.save_graph(self.med_salary_prof, path + f'{self.prefix}_year_analitic_salary.png')
        self.save_graph(self.vac_count_prof, path + f'{self.prefix}_year_analitic_count.png')
    

    def save_graph(self, df, full_path):
        df.plot()
        plt.savefig(full_path)


    def join_all(self):
        return self.med_salary.join(self.vac_count).join(self.med_salary_prof).join(self.vac_count_prof)


    def move_to_sql(self, con, table_name):
        self.joined.to_sql(con=con, name=table_name, if_exists="append")

    


df = pd.read_csv('src/csv/converted_salary.csv')
df['year'] = df['published_at'].str[:4]
df = df.drop(columns=['published_at'])

key_words = ["python", "питон", "пайтон"]

demand = DemandAnalitic(df, key_words)

# connection = sqlite3.connect('db.sqlite3')
# cur = connection.cursor()

# demand.move_to_sql(connection, 'myapp_demand')

demand.save_graphs('myapp/static/graphs/demand/')


# print("Moved to SQL")