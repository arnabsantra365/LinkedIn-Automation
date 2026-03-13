import os
import requests
from dotenv import load_dotenv

# Load the variables from .env into the environment
load_dotenv()

def save_page_html(url, filename="downloaded_job_portal_page.html"):
    if not url:
        print("Error: No URL provided in the .env file.")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Success! HTML saved to {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

# Example usage
if __name__ == "__main__":
    # Get the URL from the environment variable
    linkedInJobPortalURL = os.getenv("LINKEDIN_JOB_PORTAL_URL")
    save_page_html(linkedInJobPortalURL)