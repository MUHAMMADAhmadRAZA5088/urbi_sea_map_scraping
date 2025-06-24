import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import math

data = []
options = Options()


driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

wait = WebDriverWait(driver, 20) 

df = pd.read_csv('address.csv')
first_five = df.head(10)
for index, row in df.iterrows():
    
    driver.get("https://urbi-sa.com/riyadh?m=46.862724%2C24.622134%2F15.62")
    time.sleep(3)
    search_input = driver.find_element(By.XPATH, '//input[@class="_cu5ae4"]')
    search_input.send_keys(row["address"])
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)

    page = driver.find_element(By.XPATH, '//h2').text
    page = page.replace('Places','')


    pagination_number = int(page)/12
    pagination_number = math.ceil(pagination_number)

    for i in range(1, pagination_number+1):
        time.sleep(3)
        main_divs = driver.find_elements(By.XPATH, '//div[@class="_zjunba"]')

        for i, div in enumerate(main_divs, start=1):
            
            name = div.text
            if name == '':
                print(i)
                name = div.find_element(By.XPATH, './/span[@class="_oqoid"]').get_attribute("innerHTML")
            url = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
            try:
                id = url.split('/geo/')[1].split('?')[0]
            except:
                id = url.split('/station/')[1].split('?')[0]

            data.append({
                "name" : name,
                "id" : id,
                "url" : url
                })
        if pagination_number > 1:
            try:
                target = driver.find_element(By.XPATH, '//div[@class="_1x4k6z7"]')
                driver.execute_script("arguments[0].scrollIntoView();", target)
                time.sleep(5)
                try:
                    driver.find_element(By.XPATH,'//div[@class="_n5hmn94"][2]').click()
                except:
                    driver.find_element(By.XPATH,'//div[@class="_n5hmn94"]').click()
            except:
                pass
# Convert to pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# Optional: Save to CSV or Excel
df.to_csv("output.csv", index=False)