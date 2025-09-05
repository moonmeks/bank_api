import requests
import xml.etree.ElementTree as ET
import datetime as dt
import pandas as pd


def get_currency_data(days=90):
    end_date = dt.date.today()
    start_date = end_date - dt.timedelta(days=days)

    all_data = []

    for i in range(days + 1):
        current_date = start_date + dt.timedelta(days=i)
        date_str = current_date.strftime("%d/%m/%Y")
        url = f"http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={date_str}"

        response = requests.get(url)
        if response.status_code != 200:
            continue

        tree = ET.fromstring(response.content)
        for valute in tree.findall("Valute"):
            char_code = valute.find("CharCode").text
            name = valute.find("Name").text
            value = float(valute.find("Value").text.replace(",", "."))
            nominal = int(valute.find("Nominal").text)

            rate = value / nominal

            all_data.append(
                {"date": current_date, "code": char_code, "name": name, "rate": rate}
            )

    return pd.DataFrame(all_data)


def analyze_data(df):
    max_row = df.loc[df["rate"].idxmax()]
    min_row = df.loc[df["rate"].idxmin()]
    avg_rate = df["rate"].mean()

    print(f"""Результаты анализа за последние 90 дней:

    Максимальный курс: {max_row['name']} ({max_row['code']}) = {max_row['rate']:.4f} руб. на {max_row['date']}

    Минимальный курс: {min_row['name']} ({min_row['code']}) = {min_row['rate']:.4f} руб. на {min_row['date']}

    Среднее значение курса по всем валютам за период: {avg_rate:.4f} руб.""")

if __name__ == "__main__":
    df = get_currency_data(90)
    analyze_data(df)
