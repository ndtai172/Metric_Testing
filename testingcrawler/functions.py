import json
import time
import queue
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def scroll(speed, driver):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")


def driver_init():
    driver_options = Options()
    driver = webdriver.Chrome(options=driver_options)
    return driver


def parse_price_range(price_range):
    cleaned_price_range = price_range.replace('₫', '').replace('.', '')
    min_price, max_price = cleaned_price_range.split(' - ')

    min_price = int(min_price)
    max_price = int(max_price)

    return f"{min_price} - {max_price}"


def crawl_products(url):
    driver = driver_init()

    driver.get(url)
    # driver.implicitly_wait(20)
    time.sleep(3)
    scroll(100, driver)

    products_class = 'col-xs-2-4'
    name_class = 'APSFjk'
    price_class = 'JtW3j3'
    sold_class = 'QE5lnM'
    stars_css_selector = '.shopee-rating-stars__stars .shopee-rating-stars__star-wrapper .shopee-rating-stars__lit'

    products = driver.find_elements(By.CLASS_NAME, products_class)

    data = []
    for product in products:
        name = product.find_element(By.CLASS_NAME, name_class)
        url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        price = product.find_element(By.CLASS_NAME, price_class)
        sold = product.find_element(By.CLASS_NAME, sold_class)
        stars = product.find_elements(By.CSS_SELECTOR, stars_css_selector)

        total_percentage = 0
        for star in stars:
            style = star.get_attribute('style')
            percentage = float(style.split('width: ')[1].split('%')[0])
            total_percentage += percentage
        rating = round(total_percentage / 100, 1)

        product_data = {
            'product_name': name.text,
            'product_url': url,
            'product_price': price.text,
            'product_rating': rating,
            'product_revenue': sold.text
        }
        data.append(product_data)

    driver.close()
    return data


def crawl_categories(url):
    driver = driver_init()
    driver.get(url)
    time.sleep(3)

    categories_class = 'home-category-list__category-grid'

    categories = driver.find_elements(By.CLASS_NAME, categories_class)

    data = []

    for category in categories:
        href = category.get_attribute('href')
        category_data = {
            'url': href,
        }
        data.append(category_data)

    driver.close()
    return data


def crawl_sub_categories(url):
    driver = driver_init()
    driver.get(url)
    time.sleep(3)

    more_button_class = 'shopee-filter-group__toggle-btn'
    sub_categories_class = 'shopee-category-list__sub-category'

    more_button = driver.find_element(By.CLASS_NAME, more_button_class)
    sub_categories = driver.find_elements(By.CLASS_NAME, sub_categories_class)
    more_button.click()
    time.sleep(1)

    data = []
    main_category = {
        'url': url,
    }
    data.append(main_category)
    for sub_category in sub_categories:
        href = sub_category.get_attribute('href')
        sub_categories_data = {
            'url': href,
        }
        data.append(sub_categories_data)

    driver.close()
    return data


def crawl_with_threads(data, max_threads, crawler_func, json_filename):
    existing_data = []
    try:
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except Exception:
        pass

    crawled_data_list = []
    threads = []
    json_lock = threading.Lock()
    url_queue = queue.Queue()

    for item in data:
        url_queue.put(item)

    def crawl_thread():
        while not url_queue.empty():
            item = url_queue.get()
            crawled_data = crawler_func(item["url"])
            crawled_data_list.extend(crawled_data)
            url_queue.task_done()

    for _ in range(max_threads):
        thread = threading.Thread(target=crawl_thread)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    with json_lock:
        existing_data.extend(crawled_data_list)
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    return existing_data


def generate_urls(base_url, num_pages):
    urls = []
    for i in range(num_pages):
        page_url = f"{base_url}?page={i}"
        urls.append({"url": page_url})
    return urls


def write_to_db(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

