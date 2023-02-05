import pandas as pd

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
    def __init__(self, df, key_words) -> None:
        prof_df = get_profession_df(df, key_words)

        self.med_salary = self.__med_salary__(df)
        self.med_salary_prof = self.__med_salary__(prof_df)
        
        self.vac_count = self.__vac_count__(df)
        self.vac_count_prof = self.__vac_count__(prof_df)

        self.joined = self.join_all()

    def __med_salary__(self, df):
        med_salary = get_analitic(df, "median")
        return med_salary.rename(columns={'salary': 'med_salary'})

    def __vac_count__ (self, df):
        vac_count = get_analitic(df, "count")
        return vac_count.rename(columns={"salary": "vac_count"})

    def join_all(self):
        return self.med_salary.join(self.vac_count)
    


df = pd.read_csv('src/csv/converted_salary.csv')
df['year'] = df['published_at'].str[:4]
df = df.drop(columns=['published_at'])

key_words = ["python", "питон", "пайтон"]

demand = DemandAnalitic(df, key_words)

print(demand.joined)