import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parseHTMLtoTxt import extract_company_names

load_dotenv()

def create_driver():
    options = Options()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    return driver


def login(driver):
    login_url = os.getenv("LINKEDIN_SIGNIN_URL")
    username_env = os.getenv("USERNAME")
    password_env = os.getenv("PASSWORD")

    wait = WebDriverWait(driver, 15)

    print(f"Opening: {login_url}")
    driver.get(login_url)

    if "signup" in driver.current_url or "cold-join" in driver.current_url:
        print("Redirected to signup. Going back to login...")
        driver.get(login_url)

    print("Waiting for login fields...")
    user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    pass_field = driver.find_element(By.ID, "password")

    print("Entering credentials...")
    user_field.send_keys(username_env)
    pass_field.send_keys(password_env)
    pass_field.send_keys(Keys.RETURN)

    time.sleep(5)

    if "checkpoint" in driver.current_url:
        print("SECURITY CHECKPOINT DETECTED")
        print("Solve captcha manually")
        time.sleep(600)


def save_jobs_page(driver):
    jobs_url = os.getenv("LINKEDIN_JOB_PORTAL_URL")

    print(f"Navigating to: {jobs_url}")
    driver.get(jobs_url)

    time.sleep(15)

    filename = "actual_job_results.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"Saved jobs page to {filename}")


def main():
    driver = create_driver()

    try:
        login(driver)
        save_jobs_page(driver)
        extract_company_names("actual_job_results.html")

    except Exception as e:
        print(f"ERROR: {e}")
        driver.save_screenshot("debug_error.png")

    finally:
        print("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    main()