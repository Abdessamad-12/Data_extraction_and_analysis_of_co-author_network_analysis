import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
def get_coauthors():
    co_authors_link = driver.find_element(By.XPATH, "//a[@data-test-id='author-page-tabs__co-authors']")
    co_authors_link.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='author-influence-page__author-list__item']")))

    co_authors_list = []

    all_co_authors = driver.find_elements(By.XPATH, "//h3[@class='author-row__headline__name']")
    for co_author in all_co_authors:
        co_authors_list.append(co_author.text)
    return co_authors_list

def click_next_page(driver):
    try:
        next_page = driver.find_element(By.XPATH, "//button[@aria-label='next page' and contains(@class, 'cl-pager__button cl-pager__next')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
        time.sleep(1)  # Ensure the element is in view
        driver.execute_script("arguments[0].click();", next_page)
        return True
    except :
        print(f"ElementClickInterceptedException:. Retrying click after closing potential overlays.")
        # Close potential overlays like cookie banners
        try:
            cookie_banner = driver.find_element(By.XPATH, "//div[@class='cookie-banner']")
            if cookie_banner:
                accept_cookies_button = cookie_banner.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
                accept_cookies_button.click()
                time.sleep(2)
        except :
            pass
        # Retry clicking the next page button
        try:
            driver.execute_script("arguments[0].click();", next_page)
            return True
        except Exception as e:
            print(f"Retry failed: {e}")
            return False


authors_data = []
driver.get("https://www.semanticscholar.org/search?fos%5B0%5D=engineering&q=morocco&sort=relevance")

page_number = 1
while page_number <= 4:
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='link-button--show-visited']")))

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@data-test-id='author-list']")))
        search_authors = driver.find_elements(By.XPATH, "//span[@data-test-id='author-list']")



        all_element = driver.find_elements(By.XPATH, "//div[@class='cl-paper-row serp-papers__paper-row paper-v2-cue paper-row-normal']")
        for i in range(len(all_element)):
            results = driver.find_elements(By.XPATH, "//a[@data-test-id='title-link']")
            link_element = results[i]

            driver.execute_script("arguments[0].click();", link_element)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@data-heap-id='heap_author_list_item']")))

            all_authors = driver.find_elements(By.XPATH, "//span[@data-heap-id='heap_author_list_item']")
            for l in range(len(all_authors)):
                authors_link = driver.find_elements(By.XPATH, ".//a[@class='author-list__link author-list__author-name']")
                author = authors_link[l]
                driver.execute_script("arguments[0].click();", author)



                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@data-test-id='author-page-tabs__co-authors']")))
                author_name = driver.find_element(By.XPATH, "//h1[@data-test-id='author-name']")

                if author_name not in [data['Author'] for data in authors_data]:
                    co_authors_list = get_coauthors()
                    authors_data.append({'Author': author_name.text, 'Co-authors': ', '.join(co_authors_list)})
                driver.back()


                driver.back()




            driver.back()

        if not click_next_page(driver):
            print(f"Reached the last page or encountered an issue on page {page_number}.")
            break
        page_number += 1
    except Exception as e:
        print(f"Error on page {page_number}: {e}")
        break
with open('authors_and_coauthors.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Author', 'Co-authors']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in authors_data:
        writer.writerow(data)


time.sleep(5)
driver.quit()

