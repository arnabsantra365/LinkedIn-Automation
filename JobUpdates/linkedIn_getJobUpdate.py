import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()

def login_and_save():
    # Configuration & URLs
    login_url = os.getenv("LINKEDIN_SIGNIN_URL")
    jobs_url = os.getenv("LINKEDIN_JOB_PORTAL_URL")
    username_env = os.getenv("USERNAME")
    password_env = os.getenv("PASSWORD")

    # Chrome Options for Stealth
    options = Options()
    # Masking the automation flag
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # Use a real user agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    # Define a wait object (timeout after 15 seconds)
    wait = WebDriverWait(driver, 15)

    try:
        # Navigate to Login
        print(f"Opening: {login_url}")
        driver.get(login_url)

        # Handle Potential Signup Redirect
        if "signup" in driver.current_url or "cold-join" in driver.current_url:
            print("Detected redirect to Signup. Forcing back to Login...")
            driver.get(login_url)

        # Wait for Username Field (Explicit Wait)
        print("Waiting for login fields to appear...")
        user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        pass_field = driver.find_element(By.ID, "password")

        # Enter Credentials
        print("Entering credentials...")
        user_field.send_keys(username_env)
        pass_field.send_keys(password_env)
        pass_field.send_keys(Keys.RETURN)

        # Post-Login Check
        print("Checking for security checkpoints or successful login...")
        time.sleep(5) # Give it a moment to resolve redirects
        
        if "checkpoint" in driver.current_url:
            print("!!! SECURITY CHECKPOINT DETECTED !!!")
            print("Please solve the CAPTCHA in the browser window.")
            # We wait longer here to give you time to solve it manually if needed
            time.sleep(30) 

        # Navigate to Jobs Page
        print(f"Navigating to: {jobs_url}")
        driver.get(jobs_url)
        time.sleep(15) # Give the page a head start to render

        # Save the File
        filename = "actual_job_results.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        print(f"Success! Saved content to {filename}")

    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")
        # Save a screenshot to debug why it failed
        driver.save_screenshot("debug_error.png")
        print("Saved 'debug_error.png' - check this to see what the bot saw.")

    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    login_and_save()