import matplotlib.pyplot as plt

class GeographyAnalitic():
    """
    Represents a pandas dataframe for geography analitics
    """
    def __init__(self, df, key_words) -> None:
        df = self.__get_profession_df__(df, key_words)
        df = df.rename(columns={'area_name': 'city'})

        self.vac_count = self.__vac_count__(df)
        self.med_salary = self.__med_salary__(df)
        
        self.joined = self.med_salary.join(self.vac_count)

    
    def __get_analitic__(self, df, agg_func):
        """
        Returns a grouped dataframe by city, salary and custom aggregation function.
        :param df: DataFrame contains vacancies history
        :param agg_func: (str) aggregation function (either 'count', 'mean' or 'median')
        :return: grouped dataframe
        """
        return df.groupby("city").agg({"salary": agg_func}) 


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


    def __vac_count__ (self, df):
        """
        Gets analitic for vacancies count and renames the column
        :param df: DataFrame contains vacancies history
        :return: DataFrame contains analitic for vacancies count
        """ 

        vac_count = self.__get_analitic__(df, "count")
        vac_count = vac_count.rename(columns={"salary": 'vac_count'})
        vac_count.sort_values(by=["vac_count"], inplace=True, ascending=False)
        return vac_count.head(10)
    

    def __med_salary__(self, df):
        """
        Gets analitic for median salary in top 10 cityes by vacancies count and renames the column.
        self.vac_count must be defined.
        :param df: DataFrame contains vacancies history
        :return: DataFrame contains analitic for median salary
        """
        cityes = self.__top_10_cityes__(self.vac_count)
        df = df[df['city'].isin(cityes)]
        med_salary = self.__get_analitic__(df, "median")
        med_salary = med_salary.rename(columns={'salary': "med_salary"})
        med_salary.sort_values(by=["med_salary"], inplace=True, ascending=False)
        return med_salary


    def __top_10_cityes__(self, df):
        """
        Return top 10 cityes list by vacancies count.
        self.vac_count must be defined.
        :param df: DataFrame contains vacancies history
        :return: List of top 10 cityes by vacancies count.
        """
        df.sort_values(by=["vac_count"], inplace=True, ascending=False)
        df = df.head(10)
        return df.index.tolist()

    
    def __rename_to_rus__(self, df, dict):
        """
        Renames the columns and index in DataFrame
        :param df: DataFrame contains vacancies history
        :param dict: Dict contains words to rename as key and traslated word for value.
        :return: DataFrame with renamed columns and index 
        """
        df.index.rename('Город', inplace=True)
        return df.rename(columns=dict)

    
    def rename_all(self):
        """
        Renames all the dataframes in class using __rename_to_rus__()
        """
        self.med_salary = self.__rename_to_rus__(self.med_salary, {'med_salary': "Медианная зарплата"})
        self.vac_count = self.__rename_to_rus__(self.vac_count, {'vac_count': "Количество вакансий"})


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
        
        self.__save_graph__(self.med_salary, path + 'area_analitic_salary.png')
        self.__save_graph__(self.vac_count, path + 'area_analitic_count.png')
    

    def move_to_sql(self, con, table_name):
        """
        Append the joined DataFrame into SQL table.
        :param con: connection with sql database
        :param table_name: name of the table in SQL database.
        """
        self.joined.to_sql(con=con, name=table_name, if_exists="append")
