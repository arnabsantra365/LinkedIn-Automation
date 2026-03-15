from bs4 import BeautifulSoup
import os

def extract_company_names(html_file):
    """
    Extracts text from 'artdeco-entity-lockup__subtitle' class for company name
    'artdeco-entity-lockup__caption' for job location
    and saves it to a txt file in the same directory.
    If file exists, data will be appended.
    """

    # Read HTML file
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find all matching elements
    company_names = soup.find_all("div", class_="artdeco-entity-lockup__subtitle")
    job_locations = soup.find_all("div", class_="artdeco-entity-lockup__caption")
    job_positions = soup.find_all("div", class_="artdeco-entity-lockup__title")

    extracted_data = []

    for company, location, position in zip(company_names, job_locations, job_positions):
        company_name = company.get_text(strip=True)
        job_location = location.get_text(strip=True)
        job_role = position.find("span", attrs={"aria-hidden": "true"}).get_text(strip=True)

        extracted_data.append({
            "company": company_name,
            "location": job_location,
            "role": job_role
        })

    # Determine txt file path
    directory = os.path.dirname(html_file)
    txt_path = os.path.join(directory, "extracted_details.txt")

    # Append data to file
    with open(txt_path, "a", encoding="utf-8") as f:
        for item in extracted_data:
            f.write(f"{item['company']} | {item['location']} | {item['role']}\n")

    print(f"{len(extracted_data)} records saved to {txt_path}")
