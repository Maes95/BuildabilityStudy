from LogAnalyzerGitHub import LogAnalyzerGitHub
import concurrent.futures
from os import listdir

results_path="/home/results/GitHub/"

def checkGitHubProject(project_name):
    la = LogAnalyzerGitHub(project_name, root=results_path)
    la.analyze()

projects = [f for f in listdir(results_path)]
future_results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    for project_name in projects:
        executor.submit(checkGitHubProject, project_name)