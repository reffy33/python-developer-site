import matplotlib.pyplot as plt


class DemandAnalitic():
    def __init__(self, df, key_words, prefix="python") -> None:
        prof_df = self.__get_profession_df__(df, key_words)
        self.prefix = prefix

        self.med_salary = self.__med_salary__(df)
        self.med_salary_prof = self.__med_salary__(prof_df, prefix=True)
        
        self.vac_count = self.__vac_count__(df)
        self.vac_count_prof = self.__vac_count__(prof_df, prefix=True)

        self.joined = self.join_all()

    
    def __get_analitic__(self, df, agg_func):
        return df.groupby("year").agg({"salary": agg_func}) 


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


    def __med_salary__(self, df, prefix=False):
        med_salary = self.__get_analitic__(df, "median")
        if prefix:
            new_name = f'med_salary_{self.prefix}'
        else:
            new_name = 'med_salary'
        return med_salary.rename(columns={'salary': new_name})


    def __vac_count__ (self, df, prefix=False):
        vac_count = self.__get_analitic__(df, "count")
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
        
        self.__save_graph__(self.med_salary, path + 'year_analitic_salary.png')
        self.__save_graph__(self.vac_count, path + 'year_analitic_count.png')

        self.__save_graph__(self.med_salary_prof, path + f'{self.prefix}_year_analitic_salary.png')
        self.__save_graph__(self.vac_count_prof, path + f'{self.prefix}_year_analitic_count.png')
    

    def __save_graph__(self, df, full_path):
        df.plot()
        plt.savefig(full_path)


    def join_all(self):
        return self.med_salary.join(self.vac_count).join(self.med_salary_prof).join(self.vac_count_prof)


    def move_to_sql(self, con, table_name):
        self.joined.to_sql(con=con, name=table_name, if_exists="append")
