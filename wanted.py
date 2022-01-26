import requests as req
from bs4 import BeautifulSoup

# 파이썬 개발자 : 518/899
# 웹개발자 : 518/873
# nodejs 개발자 : 518/895
# 자바 개발자: 518/660

KEYWORD = "python"
URL = f"https://www.wanted.co.kr/wdlist/518/899?country=kr&job_sort=job.latest_order&years=-1&locations=all"


def get_job(html):
    # span 태그의 title 속성의 경우 제목이 들어가기에 값을 가져올려면 title 속성이 있는 것만 가져와서 string만 가져오는 식으로
    title = html.find("span", {"title": True}).string
    # 인디드는 타이틀에 회사이름이 안 들어가 있는 경우도 있고, 중복된 타이틀도 있어서 회사명도 스크래핑함
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
        company = None
    location = html.find("div", {"class" : "companyLocation"}).string
    job_id = html["data-jk"]
    return {
        "title": title,
        "company": company,
        "location" : location,
        "link" : f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


# 파싱한 결과에서 데이터 추출하는 함수
def get_jobs_wanted():
    jobs = []
    res = req.get(f"{URL}")
    soup = BeautifulSoup(res.text, "html.parser")

    # 파싱한 정보에서 일자리 정보 가져오기
    result = soup.find("div", {"class":"List"})
    print(soup)
    # 일자리 정보가 담긴 배열을 순회하면서 정보를 가져오고 jobs 배열에 추가 후 리턴
    # for info in infos:
    #     jobs.append(get_job(info))
    # return jobs
