import requests as req
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


# 스크래핑한 페이지들의 마지막 페이지를 리턴하는 함수
def extract_indeed_pages():
    # 'python'에 대한 검색결과 1페이지당 50개씩
    res = req.get(URL)

    indeed_soup = BeautifulSoup(res.text, 'html.parser')
    pagination = indeed_soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")

    # 페이지 숫자를 담을 배열 생성
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    # 마지막 페이지
    max_page = pages[-1]
    return max_page


def extract_job(html):
    # span 태그의 title 속성의 경우 제목이 들어가기에 값을 가져올려면 title 속성이 있는 것만 가져와서 string만 가져오는 식으로
    title = html.find("span", {"title": True}).string
    # 인디드는 타이틀에 회사이름이 안 들어가 있는 경우도 있고, 중복된 타이틀도 있어서 회사명도 스크래핑함
    company = html.find("span", {"class": "companyName"}).string
    return {"title": title, "company": company}


# 검색한 결과의 페이지에서 회사와 일자리 추출하는 함수
def extract_indeed_jobs(last_page):
    jobs = []
    res = req.get(f"{URL}&start={0 * LIMIT}")
    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("td", {"class" : "resultContent"})

    for result in results:
        jobs.append(extract_job(result))
    return jobs