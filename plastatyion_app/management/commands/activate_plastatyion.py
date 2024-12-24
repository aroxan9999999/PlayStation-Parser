from django.core.management.base import BaseCommand
from plastatyion_app.models import Product
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
from decimal import Decimal, InvalidOperation
from datetime import datetime

class Command(BaseCommand):
    help = "Парсинг продуктов PlayStation и сохранение их в базу данных."

    def handle(self, *args, **kwargs):
        self.parse_with_selenium_and_bs4()

    def clean_price(self, price_str):
        cleaned_price = re.sub(r'[^\d,]', '', price_str)
        cleaned_price = cleaned_price.replace(',', '.')
        try:
            return Decimal(cleaned_price)
        except InvalidOperation:
            return None


    def parse_with_selenium_and_bs4(self, step=253):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        base_url = "https://store.playstation.com/en-tr/category/83a687fe-bed7-448c-909f-310e74a71b39/"

        for i in range(1, step + 1):
            url = f"{base_url}{i}"
            driver.get(url)
            time.sleep(3)

            try:
                # Получаем HTML-код страницы
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Ищем ul с классом psw-grid-list psw-l-grid
                grid_list = soup.find('ul', class_='psw-grid-list psw-l-grid')

                if not grid_list:
                    print(f"Продукты не найдены на странице {i}")
                    continue

                product_elements = grid_list.find_all('li')
                print(f"Страница {i}: найдено {len(product_elements)} продуктов")
                for product_index, product in enumerate(product_elements, start=1):
                    print(f"--- Обрабатываем продукт #{product_index} ---")
                    try:
                        # Получаем ссылку на продукт
                        link_tag = product.find('a', class_='psw-link psw-content-link')
                        product_url = link_tag['href'] if link_tag else ""
                        full_url = f"https://store.playstation.com{product_url}" if product_url else None

                        img_tags = product.find_all("img")
                        photo = img_tags[0].get('src', 'неизвестно') if img_tags else "Фото не найдено"

                        # Перейдем по ссылке продукта для деталей
                        if full_url:
                            one_product_page = requests.get(full_url)
                            product_page_source = one_product_page.content
                            product_soup = BeautifulSoup(product_page_source, 'html.parser')

                            # Название
                            name_tag = product_soup.find('h1', {'data-qa': 'mfe-game-title#name'})
                            name = name_tag.text.strip() if name_tag else "Название не найдено"

                            # Текущая цена
                            current_price_tag = product_soup.find('span', class_='psw-t-title-m psw-m-r-4')
                            current_price = self.clean_price(current_price_tag.text.strip() if current_price_tag else "Цнеизвестныйа")

                            # Старая цена
                            old_price_tag = product_soup.find('span', class_='psw-t-title-s psw-c-t-2 psw-t-strike')
                            old_price = self.clean_price(old_price_tag.text.strip() if old_price_tag else 'неизвестный')

                            # Скидка
                            discount_tag = product_soup.find('span', class_='psw-m-r-3')
                            discount = discount_tag.text.strip() if discount_tag else None

                            # Дата окончания акции,

                            end_date_tag = product_soup.find('span', text=re.compile('^Offer ends'))
                            date = end_date_tag.text.strip().split(' ')[2]

                            # Сохраняем данные в базу
                            product, created = Product.objects.update_or_create(
                                product_url=full_url,
                                defaults={
                                    'name': name,
                                    'current_price': current_price,
                                    'old_price': old_price,
                                    'discount': discount.split(' ')[1],
                                    'offer_end_date': datetime.strptime(date, "%d/%m/%Y").date(),
                                    'photo_url': photo,
                                },
                            )
                            action = "Создан" if created else "Обновлен"
                            print(f"{action}: {product.name}")
                        else:
                            print("Пропущен продукт без ссылки.")
                    except Exception as e:
                        print(f"Ошибка при обработке продукта #{product_index}: {e}")
                print(f"Обработано {len(product_elements)} продуктов на странице {i}")
            except Exception as e:
                print(f"Ошибка на странице {i}: {e}")
                break

        driver.quit()
