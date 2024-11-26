import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка WebDriver
driver = webdriver.Chrome()
url = "https://www.divan.ru/petrozavodsk/category/svet"
driver.get(url)
time.sleep(3)
# Ожидание загрузки товаров
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.WdR1o'))
    )
except Exception as e:
    print(f"Ошибка ожидания элементов: {e}")
    driver.quit()
    exit()

# Сбор данных
parsed_data = []

goods = driver.find_elements(By.CSS_SELECTOR, 'div.WdR1o')
for good in goods:
    try:
        # Извлечение названия
        name_element = good.find_element(By.CSS_SELECTOR, 'a.qUioe')
        name = name_element.text.strip() if name_element.text else "Нет названия"

        # Извлечение цены
        price_element = good.find_element(By.CSS_SELECTOR, 'span.KIkOH')
        price = price_element.text.strip() if price_element.text else "Нет цены"

        # Извлечение ссылки
        link_element = good.find_element(By.CSS_SELECTOR, 'a')
        link = link_element.get_dom_attribute('href')

        # Добавление в список
        parsed_data.append([name, price, link])

    except Exception as e:
        print(f"Произошла ошибка при парсинге товара: {e}")
        continue

# Завершение работы WebDriver
driver.quit()

# Сохранение данных в CSV
with open("light.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Название товара', 'Цена товара', 'Ссылка на товар'])
    writer.writerows(parsed_data)

print("Парсинг завершен. Данные сохранены в light.csv.")
