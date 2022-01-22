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
    print(title)
    company = html.find("span", {"class" : "companyName"})
    # span 태그 안에 a 태그가 있는 경우도 있어서 조건을 나눔
    # 또한 회사이름이 없는 것도 있어서 그 부분 조건도 추가
    # company가 Nonetype이 아닐 시
    if company is not None:
        # company 안에 a 태그의 내용에서 회사 이름을 가져오고
        company_anchor = company.find("a", {"data-tn-element": "companyName"})
        # 존재할 시엔 a 태그에 있는 회사이름을
        if company_anchor is not None:
            company = str(company_anchor.string)
        # 없을시 처음 가져왔던 회사 이름을
        elif company is not None:
            company = str(company.string)
    else: # 회사 이름이 존재하지 않을 시 빈 문자열의 값을 할당했다.
        company = ""
    location = html.find("div", {"class" : "companyLocation"}).string
    job_id = html["data-jk"]
    return {
        "title": title,
        "company": company,
        "location" : location,
        "link" : f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


# 검색한 결과의 페이지에서 회사와 일자리 추출하는 함수
def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        # print(f"Scrapping page: {page}")
        res = req.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(res.text, "html.parser")
        # 파싱한 정보에서 일자리 정보 가져오기
        get_job_info = soup.find("div", {"id": "mosaic-provider-jobcards"})
        # 앵커 태그들을 한 개씩 담는 배열로 생성
        infos = get_job_info.find_all("a", {"class" : "resultWithShelf"})
        # 일자리 정보가 담긴 배열을 순회하면서 정보를 가져오고 jobs 배열에 추가 후 리턴
        for info in infos:
            jobs.append(extract_job(info))
    return jobs