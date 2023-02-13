import matplotlib.pyplot as plt


class DemandAnalitic():
    """
    Represents a pandas dataframe for demand analitics
    """
    def __init__(self, df, key_words, prefix="python") -> None:
        prof_df = self.__get_profession_df__(df, key_words)
        self.prefix = prefix

        self.med_salary = self.__med_salary__(df)
        self.med_salary_prof = self.__med_salary__(prof_df, prefix=True)
        
        self.vac_count = self.__vac_count__(df)
        self.vac_count_prof = self.__vac_count__(prof_df, prefix=True)

        self.joined = self.join_all()

    
    def __get_analitic__(self, df, agg_func):
        """
        Returns a grouped dataframe by year, salary and custom aggregation function.
        :param df: DataFrame contains vacancies history
        :param agg_func: (str) aggregation function (either 'count', 'mean' or 'median')
        :return: grouped dataframe
        """
        return df.groupby("year").agg({"salary": agg_func}) 


    def __get_profession_df__(self, df, key_words):
        """
        Filter a dataframe leaving only vacancies with metioned key words
        :param df: DataFrame contains vacancies history
        :param key_words: (list) list of key words to look in dataframe
        :return: dataframe with only vacancies featuring key words
        """
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
        """
        Gets analitic for median salary and renames the column
        :param df: DataFrame contains vacancies history
        :param prefix=False: True for adding prefix to the name of a column and False for not adding.
        :return: DataFrame contains analitic for median salary
        """ 
        med_salary = self.__get_analitic__(df, "median")
        if prefix:
            new_name = f'med_salary_{self.prefix}'
        else:
            new_name = 'med_salary'
        return med_salary.rename(columns={'salary': new_name})


    def __vac_count__ (self, df, prefix=False):
        """
        Gets analitic for vacancies count and renames the column
        :param df: DataFrame contains vacancies history
        :param prefix=False: True for adding prefix to the name of a column and False for not adding.
        :return: DataFrame contains analitic for vacancies count
        """ 
        vac_count = self.__get_analitic__(df, "count")
        if prefix:
            new_name = f'vac_count_{self.prefix}'
        else:
            new_name = 'vac_count'
        return vac_count.rename(columns={"salary": new_name})

    
    def __rename_to_rus__(self, df, dict):
        """
        Renames the columns and index in DataFrame
        :param df: DataFrame contains vacancies history
        :param dict: Dict contains words to rename as key and traslated word for value.
        :return: DataFrame with renamed columns and index 
        """
        df.index.rename('Год', inplace=True)
        return df.rename(columns=dict)

    
    def rename_all(self):
        """
        Renames all the dataframes in class using __rename_to_rus__()
        """
        self.med_salary = self.__rename_to_rus__(self.med_salary, {'med_salary': "Медианная зарплата"})
        self.med_salary_prof = self.__rename_to_rus__(self.med_salary_prof, {f'med_salary_{self.prefix}': 'Медианная зарплата'})

        self.vac_count = self.__rename_to_rus__(self.vac_count, {'vac_count': "Количество вакансий"})
        self.vac_count_prof = self.__rename_to_rus__(self.vac_count_prof, {f'vac_count_{self.prefix}': "Количество вакансий"})


    def __save_graph__(self, df, full_path):
        """
        Saves a simple matplotlib plot 
        :param df: DataFrame to save the graph from
        :param full_path: path to file
        """
        df.plot()
        plt.savefig(full_path)


    def save_graphs(self, path, traslate=True):
        """
        Saves all the graphs with all classes DataFrames
        :param path: path to directory where to save the files, without the file name
        :param traslate=True: True to rename the field, False to not to rename, uses rename_all()
        """
        if traslate:
            self.rename_all()
        
        self.__save_graph__(self.med_salary, path + 'year_analitic_salary.png')
        self.__save_graph__(self.vac_count, path + 'year_analitic_count.png')

        self.__save_graph__(self.med_salary_prof, path + f'{self.prefix}_year_analitic_salary.png')
        self.__save_graph__(self.vac_count_prof, path + f'{self.prefix}_year_analitic_count.png')
    

    def join_all(self):
        """
        Return a DataFrame contains all the info needed for analitic and import to sql table
        """
        return self.med_salary.join(self.vac_count).join(self.med_salary_prof).join(self.vac_count_prof)


    def move_to_sql(self, con, table_name):
        """
        Append the joined DataFrame into SQL table.
        :param con: connection with sql database
        :param table_name: name of the table in SQL database.
        """
        self.joined.to_sql(con=con, name=table_name, if_exists="append")
