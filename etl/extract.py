import pandas as pd
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from etl.logger import logging, timed, section

BASE_URL = "https://findajob.dwp.gov.uk/search?loc=86383&q=data%20engineer&page="
OUTPUT_FOLDER = Path("data/job_listings")


def path_to_csv():
    if not OUTPUT_FOLDER.exists():
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    return OUTPUT_FOLDER / "job_listings.csv"


def extract_job_listings(url):
    url = "https://findajob.dwp.gov.uk/search?q=data+engineer&loc=86383"

    response = requests.get(url)

    titles = []
    link = []
    date_posted = []
    company = []
    location = []
    salary = []

    soup = BeautifulSoup(response.content, 'html.parser')

    job_listings = soup.find_all('div', class_='search-result')

    for job in job_listings:
        # Titles
        title_element = job.find('a', class_='govuk-link')
        if title_element:
            titles.append(title_element.text.strip())
            link.append(title_element['href'])

        # Date Posted
        date_element = job.find('li')
        if date_element:
            date_posted.append(date_element.text.strip())

        # Company
        company_name = job.find('strong')
        if company_name:
            company.append(company_name.text.strip())

        # Location
        location_element = job.find('span')
        if location_element:
            location.append(location_element.text.strip())

        # Salary
        salary_element = job.find(
            'li', string=lambda text: text and '£' in text)
        if salary_element:
            salary.append(salary_element.text.strip())
        else:
            salary.append('Not specified')

    return pd.DataFrame({
        'Title': titles,
        'Link': link,
        'Date Posted': date_posted,
        'Company': company,
        'Location': location,
        'Salary': salary
    })


def save_to_csv(df, filename):
    filename = path_to_csv()
    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")


@timed
def main():
    section("Extracting Job Listings")
    df = extract_job_listings(BASE_URL)
    save_to_csv(df, path_to_csv())
    logging.info(f"\033[92m🎉 Data extraction complete. Sample data:\033[0m")
    logging.info(df.head())
    logging.info(f"Total job listings extracted: {len(df)}")


if __name__ == "__main__":
    main()
