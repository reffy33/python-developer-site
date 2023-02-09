import matplotlib.pyplot as plt
import pandas as pd
import sqlite3


class GeographyAnalitic():
    def __init__(self, df, key_words) -> None:
        df = self.__get_profession_df__(df, key_words)
        df = df.rename(columns={'area_name': 'city'})

        self.vac_count = self.__vac_count__(df)
        self.med_salary = self.__med_salary__(df)
        
        self.joined = self.med_salary.join(self.vac_count)

    
    def __get_analitic__(self, df, agg_func):
        return df.groupby("city").agg({"salary": agg_func}) 


    def __get_profession_df__(self, df, key_words):
        first = True
        for word in key_words:
            if first:
                first = False
                mask = df["name"].str.contains(word)
            else:
                new_mask = df["name"].str.contains(word)
                mask = mask | new_mask

        return df.loc[mask]


    def __med_salary__(self, df):
        cityes = self.__top_10_cityes__(self.vac_count)
        df = df[df['city'].isin(cityes)]
        med_salary = self.__get_analitic__(df, "median")
        med_salary = med_salary.rename(columns={'salary': "med_salary"})
        med_salary.sort_values(by=["med_salary"], inplace=True, ascending=False)
        return med_salary


    def __vac_count__ (self, df):
        vac_count = self.__get_analitic__(df, "count")
        return vac_count.rename(columns={"salary": 'vac_count'})

    
    def __top_10_cityes__(self, df):
        df.sort_values(by=["vac_count"], inplace=True, ascending=False)
        df = df.head(10)
        return df.index.tolist()

    
    def __rename_to_rus__(self, df, dict):
        df.index.rename('Город', inplace=True)
        return df.rename(columns=dict)

    
    def rename_all(self):
        self.med_salary = self.__rename_to_rus__(self.med_salary, {'med_salary': "Медианная зарплата"})
        self.vac_count = self.__rename_to_rus__(self.vac_count, {'vac_count': "Количество вакансий"})


    def save_graphs(self, path, traslate=True):
        if traslate:
            self.rename_all()
        
        
        self.save_graph(self.med_salary, path + 'area_analitic_salary.png')
        self.save_graph(self.vac_count, path + 'area_analitic_count.png')
    

    def save_graph(self, df, full_path):
        df.plot()
        plt.savefig(full_path)


    def move_to_sql(self, con, table_name):
        self.joined.to_sql(con=con, name=table_name, if_exists="append")


df = pd.read_csv('src/csv/converted_salary.csv')
df['year'] = df['published_at'].str[:4]
df = df.drop(columns=['published_at'])

key_words = ["python", "питон", "пайтон"]

geo = GeographyAnalitic(df, key_words)

geo.save_graphs('myapp/static/graphs/geography/')
print("Graphs saved")