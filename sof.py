import requests as req
from bs4 import BeautifulSoup


URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = req.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class":"fs-body3"}).find("a")["title"]
    company = html.find("h3", {"class": "fs-body1"}).find("span", {"class": "fc-black-500"}).text
    return { "title": title, "company": company }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = req.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for res in results:
            job = extract_job(res)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return []