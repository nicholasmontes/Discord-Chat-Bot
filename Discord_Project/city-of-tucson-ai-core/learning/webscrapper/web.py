from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List of URLs to scrape
urls = [
    "https://aicore.arizona.edu/",
    "https://aicore.arizona.edu/portfolio",
    "https://aicore.arizona.edu/speaking",
    "https://aicore.arizona.edu/work-with-us"

]

driver = webdriver.Chrome()  # Make sure the ChromeDriver is in your PATH


def scrape_page(url):
    driver.get(url)
    # Wait for the JavaScript to load and the body element to be present
    main_content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Remove header & footer if it exists
    try:
        header = main_content.find_element(By.TAG_NAME, 'header')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, header)
    except:
        pass 

    try:
        footer_container = main_content.find_element(By.CLASS_NAME, 'footer_container')
        driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, footer_container)
    except:
        pass  

    # Get the text content from the remaining body
    page_text = main_content.text

    return page_text

try:
    all_text = ""
    for url in urls:
        print(f"Scraping {url}")
        page_text = scrape_page(url)
        all_text += page_text + "\n\n"  # Separate content from different pages

    with open("aicore_website.txt", "w", encoding="utf-8") as file:
        file.write(all_text)

    print("Webpages text saved to aicore_website.txt")

finally:
    driver.quit()
