from indeed import get_jobs as get_indeed_jobs
from wanted import get_jobs_wanted

keyword = "python"
indeed_jobs = get_indeed_jobs(keyword)
# print(parsing_wanted())
print(get_jobs_wanted())

