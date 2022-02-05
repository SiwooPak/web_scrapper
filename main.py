from indeed import get_jobs as get_indeed_jobs
#from wanted import get_jobs_wanted
from sof import get_jobs as get_sof_jobs


keyword = "python"
indeed_jobs = get_indeed_jobs(keyword)
sof_jobs = get_sof_jobs()
jobs = { "indeed": indeed_jobs, "sof": sof_jobs}
print(jobs)
