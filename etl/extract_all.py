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

    return OUTPUT_FOLDER / "job_listings_all.csv"


def extract_job_listings(url):
    pages = range(1, 19)

    titles = []
    link = []
    posting_date = []
    company = []
    location = []
    salary = []
    job_type = []

    for page in pages:
        logging.info(f"Extracting data from page {page}...")
        page_url = url + str(page)
        logging.info(f"Extracting data from: {page_url}")

        response = requests.get(page_url)

        if response.status_code != 200:
            logging.error(
                f"Failed to fetch page {page}: Status code {response.status_code}")
            continue

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all job listings on the page
        job_listings = soup.find_all("div", class_="search-result")

        logging.info(f"Found {len(job_listings)} jobs on page {page}\n")

        for job in job_listings:
            # Extract job title and link
            title_element = job.find("a", class_="govuk-link")
            if title_element:
                titles.append(title_element.text.strip())

                href = title_element.get("href")
                if href and href.startswith("/"):
                    link.append("https://findajob.dwp.gov.uk" + href)
                else:
                    link.append(href)

            # Extract date posted
            date_element = job.find("li")
            if date_element:
                posting_date.append(date_element.text.strip())
            else:
                posting_date.append("Not specified")

            # Extract company name
            company_name = job.find("strong")
            if company_name:
                company.append(company_name.text.strip())
            else:
                company.append("Not specified")

            # Extract location
            location_element = job.find("span")
            if location_element:
                location.append(location_element.text.strip())
            else:
                location.append("Not specified")

            # Extract salary
            salary_element = job.find(
                "li", string=lambda text: text and "£" in text)
            if salary_element:
                salary.append(salary_element.text.strip())
            else:
                salary.append("Not specified")

            # Extract job type
            job_type_element = job.find(
                "li", class_="govuk-tag govuk-tag--grey govuk-!-margin-right-1 govuk-!-margin-top-1 govuk-!-font-weight-regular job-tag-font-override")
            if job_type_element:
                job_type.append(job_type_element.text.strip())
            else:
                job_type.append("Not specified")

    return pd.DataFrame({
        "Title": titles,
        "Link": link,
        "Date Posted": posting_date,
        "Company": company,
        "Location": location,
        "Salary": salary,
        "Job Type": job_type
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
    logging.info(f"\033[92m🎉 Data extraction complete. Sample data:\033[0m\n")
    logging.info(df.head())
    logging.info(f"\033[92mTotal job listings extracted: {len(df)}\033[0m\n")


if __name__ == "__main__":
    main()
