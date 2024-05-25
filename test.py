import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_coauthors(driver):
    co_authors_link = driver.find_element(By.XPATH, "//a[@data-test-id='author-page-tabs__co-authors']")
    co_authors_link.click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='author-influence-page__author-list__item']"))
    )
    co_authors_list = [co_author.text for co_author in
                       driver.find_elements(By.XPATH, "//h3[@class='author-row__headline__name']")]
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


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.semanticscholar.org/search?fos%5B0%5D=engineering&q=morocco&sort=relevance")
authors = []
page_number = 1

while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='link-button--show-visited']")))

        paper_rows = driver.find_elements(By.XPATH,
                                          "//div[@class='cl-paper-row serp-papers__paper-row paper-v2-cue paper-row-normal']")
        for i in range(len(paper_rows)):
            try:
                results = driver.find_elements(By.XPATH, "//a[@data-test-id='title-link']")
                if i < len(results):
                    link_element = results[i]
                    driver.execute_script("arguments[0].click();", link_element)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[@data-heap-id='heap_author_list_item']"))
                    )

                    author_elements = driver.find_elements(By.XPATH,
                                                           "//span[@data-heap-id='heap_author_list_item']//a[@class='author-list__link author-list__author-name']")
                    for j in range(len(author_elements)):
                        try:
                            if j < len(author_elements):
                                author_element = author_elements[j]
                                driver.execute_script("arguments[0].click();", author_element)

                                WebDriverWait(driver, 20).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//a[@data-test-id='author-page-tabs__co-authors']")))

                                author_name_element = driver.find_element(By.XPATH, "//h1[@data-test-id='author-name']")
                                author_name = author_name_element.text

                                if author_name not in authors:
                                    authors.append(author_name)
                                    co_authors_list = get_coauthors(driver)
                                    authors_data = [author_name, co_authors_list]
                                    print(authors_data)
                                    driver.back()

                                driver.back()
                        except Exception as e:
                            print(f"Error processing author on page {page_number}, index {j}: {e}")
                            driver.back()

                    driver.back()
            except Exception as e:
                print(f"Error processing paper row on page {page_number}, index {i}: {e}")
                driver.back()

        if not click_next_page(driver):
            print(f"Reached the last page or encountered an issue on page {page_number}.")
            break
        page_number += 1

    except Exception as e:
        print(f"Error on page {page_number}: {e}")
        break

time.sleep(5)
driver.quit()
