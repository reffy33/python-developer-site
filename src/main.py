import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

from convert_salary import convert_salary


def get_analitic(df, group_by, agg_func):
    return df.groupby(group_by).agg({'salary': agg_func})


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


def demand_analitic(df):
    year_analitic_salary = get_analitic(df, "year", "median").rename(columns={'salary': 'med_salary'})
    year_analitic_count = get_analitic(df, "year", "count").rename(columns={"salary": "vac_count"})
    year_analitic = year_analitic_salary.join(year_analitic_count)

    python_df = get_profession_df(df, ["python", "питон", "пайтон"])

    python_year_analitic_salary = get_analitic(python_df, "year", "median").rename(
        columns={'salary': 'med_salary_python'})
    year_analitic = year_analitic.join(python_year_analitic_salary)

    python_year_analitic_count = get_analitic(python_df, "year", "count").rename(
        columns={"salary": "vac_count_python"})
    year_analitic = year_analitic.join(python_year_analitic_count)

    path = '../myapp/static/myapp/graphs/'
    year_analitic_salary = year_analitic_salary.rename(columns={'med_salary': "Медианная зарплата"})
    year_analitic_salary.index.rename('Год', inplace=True)
    year_analitic_salary.plot()
    plt.savefig(path + 'year_analitic_salary.png')

    year_analitic_count = year_analitic_count.rename(columns={'vac_count': "Количество вакансий"})
    year_analitic_count.index.rename('Год', inplace=True)
    year_analitic_count.plot()
    plt.savefig(path + 'year_analitic_count.png')

    python_year_analitic_salary = python_year_analitic_salary.rename(
        columns={'med_salary_python': "Медианная зарплата"})
    python_year_analitic_salary.index.rename('Год', inplace=True)
    python_year_analitic_salary.plot()
    plt.savefig(path + 'python_year_analitic_salary.png')

    python_year_analitic_count = python_year_analitic_count.rename(columns={'vac_count_python': "Количество вакансий"})
    python_year_analitic_count.index.rename('Год', inplace=True)
    python_year_analitic_count.plot()
    plt.savefig(path + 'python_year_analitic_count.png')

    return year_analitic


def geograpy_analitic(df):
    df = get_profession_df(df, ["python", "питон", "пайтон"])
    df = df.rename(columns={'area_name': 'city'})

    area_analitic_count = df.groupby(['city']).agg({'salary': 'count'})
    area_analitic_count = area_analitic_count.rename(columns={'salary': "vac_count"})

    area_analitic_count.sort_values(by=["vac_count"], inplace=True, ascending=False)
    area_analitic_count = area_analitic_count.head(10)

    cityes = area_analitic_count.index.tolist()

    area_analitic_salary = df[df['city'].isin(cityes)]
    area_analitic_salary = area_analitic_salary.groupby(['city']).agg({'salary': 'median'})
    area_analitic_salary = area_analitic_salary.rename(columns={'salary': "med_salary"})

    path = '../myapp/static/myapp/graphs/'

    area_analitic_count = area_analitic_count.rename(columns={'vac_count': "Количество вакансий"})
    area_analitic_count.index.rename('Город', inplace=True)
    area_analitic_count.plot()
    plt.savefig(path + 'area_analitic_count.png')

    area_analitic_salary.sort_values(by=["med_salary"], inplace=True, ascending=False)
    area_analitic_salary = area_analitic_salary.rename(columns={'med_salary': "Медианная зарплата"})
    area_analitic_salary.index.rename('Город', inplace=True)
    area_analitic_salary.plot()
    plt.savefig(path + 'area_analitic_salary.png')

    return area_analitic_salary.join(area_analitic_count)


def main():
    # df = convert_salary("csv/vacancies_with_skills.csv", 'csv/currensies_history.csv')
    df = pd.read_csv('csv/converted_salary.csv')

    df['year'] = df['published_at'].str[:4]
    df = df.drop(columns=['published_at'])

    connection = sqlite3.connect('../db.sqlite3')
    cur = connection.cursor()

    year_analitic = demand_analitic(df)
    year_analitic.to_sql(con=connection, name='myapp_demand', if_exists="append")

    area_analitic = geograpy_analitic(df)
    area_analitic.to_sql(con=connection, name='myapp_geography', if_exists="append")


if __name__ == "__main__":
    main()
