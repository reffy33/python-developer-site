import pandas as pd


def convert_cur(salary, publ_date, cur, cur_history):
    """
    Конвертирует сумму в рубли, по курсу на момент публикации
    :param salary: сумма
    :param publ_date: дата публикации
    :param cur: валюта
    :param cur_history: (dataframe) история изменения курсов валют
    :return: округлённая до 1 знака после запятой сумма
    """
    if cur == 'RUR':
        return salary
    elif cur not in cur_history.columns:
        return 0
    return round(salary * cur_history[cur][publ_date[:7]], 1)


def convert_salary(input_file, cur_history_file):
    """
    Изменяет dataframe, создавая новый столбец salary в котором хранится зарплата перевённая в рубли, данные получены
    из столбцов salary_from, salary_to и salary_currency
    :param input_file: имя входного файла
    :param cur_history_file: имя файла хранящего историю изменения курса валют
    """
    cur_history = pd.read_csv(cur_history_file, index_col=0)
    vacancies = pd.read_csv(input_file)
    print('Files read')

    vacancies = vacancies[vacancies['salary_currency'].notna()]
    print('NaN rows deleted')
    vacancies['salary'] = 0

    mask1 = (vacancies['salary_from'].isnull() & ~vacancies['salary_to'].isnull())
    vacancies['salary'][mask1] = vacancies['salary_to']
    mask2 = (~vacancies['salary_from'].isnull() & vacancies['salary_to'].isnull())
    vacancies['salary'][mask2] = vacancies['salary_from']
    print('Salary row created')

    vacancies['salary'] = vacancies.apply(
        lambda x: convert_cur(x.salary, x.published_at, x.salary_currency, cur_history), axis=1)
    print('Salarys converted')

    vacancies = vacancies[vacancies.salary != 0]
    vacancies = vacancies.drop(columns=['salary_to', 'salary_from', 'salary_currency'])
    print('Dataframe ready')
    return vacancies


def main():
    convert_salary('csv/vacancies_dif_currencies.csv', 'csv/currensies_history.csv')


if __name__ == '__main__':
    main()