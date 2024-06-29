import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ChromeDriver 路径
chrome_driver_path = "/Users/devdev/Desktop/SIDEPROJECTS/FootyStatsPy/chromedriver"

print(f"Using ChromeDriver from path: {chrome_driver_path}")

# Configurar ChromeDriver
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Inicializar WebDriver
try:
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    print("ChromeDriver initialized successfully.")
except Exception as e:
    print(f"Error initializing ChromeDriver: {e}")

# Función para obtener las columnas del DataFrame
def get_columns_df(soup, table_name):
    lst = []  # Para almacenar los nombres de las columnas
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

# Función para obtener los datos de fbref
def get_data_fbref(url, table_name):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        df = get_columns_df(soup, table_name)
        index = 0
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
    except TimeoutException:
        print(f"Timeout while accessing {url}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return pd.DataFrame()

# Función principal para scrape_euro2024_data
def scrape_euro2024_data():
    urls = ["https://fbref.com/en/comps/676/schedule/European-Championship-Scores-and-Fixtures"]
    table_ids = ["stats", "keepers", "shots_all"]
    data_dict = {}

    for url in urls:
        for table_id in table_ids:
            print(f"Scraping data for {table_id} from {url}")
            df = get_data_fbref(url, table_id)
            if not df.empty:
                data_dict[f"{table_id}_euro2024"] = df
                time.sleep(5)  # Dormir para evitar ser bloqueado
            else:
                print(f"Failed to scrape data for {table_id} from {url}. Retrying after a delay.")
                time.sleep(300)

    if data_dict:
        final_df = pd.concat(data_dict.values(), ignore_index=True)
        return final_df
    else:
        return pd.DataFrame()

if __name__ == '__main__':
    data = scrape_euro2024_data()
    if not data.empty:
        data.to_csv("euro2024_data.csv", index=False)
        print("Data scraped successfully and saved to euro2024_data.csv")
    else:
        print("Failed to scrape any data.")
