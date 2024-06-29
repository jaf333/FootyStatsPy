import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_columns_df(r, table_name):
    lst = []  # To append columns' names
    soup = BeautifulSoup(r.content, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        if table.get('id') and str(table.get('id')).endswith(table_name):
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                for col in columns:
                    data_stat = col.get("data-stat")
                    if data_stat and data_stat not in lst:
                        lst.append(str(data_stat))
        elif table_name == "keeper" and "keeper" in str(table.get('id')):
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                for col in columns:
                    data_stat = col.get("data-stat")
                    if data_stat and data_stat not in lst:
                        lst.append(str(data_stat))
    return pd.DataFrame(columns=lst)

def get_data_fbref(url, table_name):
    rq = requests.session().get(url)
    soup = BeautifulSoup(rq.text, "html.parser")
    index = 0
    df = get_columns_df(rq, table_name)
    tables = soup.find_all("table")

    for table in tables:
        if table_name == "shots_all" and table.get('id') == "shots_all":
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                row_data = [columns[j].text for j in range(len(columns))]
                df.loc[len(df)] = row_data

        elif table_name == "keeper" and "keeper" in str(table.get('id')):
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                row_data = [columns[j].text for j in range(len(columns))]
                df.loc[len(df)] = row_data

        elif table.get('id') and str(table.get('id')).endswith(table_name):
            for row in table.tbody.find_all('tr'):
                names = row.find_all('th')
                player_name = None
                for name in names:
                    player_name = name.get('csk')
                if player_name:
                    df.loc[index, "name"] = player_name

                columns = row.find_all('td')
                for j in range(len(columns)):
                    if player_name:
                        df.iloc[index, j] = columns[j].text
                index += 1

    df["match"] = url.split("/")[6]
    return df

def scrape_euro2024_data():
    urls = ["https://fbref.com/en/comps/676/schedule/European-Championship-Scores-and-Fixtures"]
    table_ids = ["stats", "keepers", "shots_all"]
    data_dict = {}
    i = 0

    for url in urls:
        for table_id in table_ids:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Scraping data for {table_id} from {url}")
                data_dict[f"{table_id}_euro2024"] = get_data_fbref(url, table_id)
                i += 1
                time.sleep(5)  # Sleep to avoid being blocked
            else:
                print(f"Failed to access {url}. Retrying after a delay.")
                time.sleep(300)

    final_df = pd.concat(data_dict.values(), ignore_index=True)
    return final_df
