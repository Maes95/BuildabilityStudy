import csv
import pandas as pd
import re
import hashlib
import os
import json
import subprocess

MAVEN_COMMON_ERRORS_MAP = {}
with open('/home/previousResults/maven-common-errors.txt', "r") as f:
    for line in f.readlines():
        exception, action = line.rstrip("\n").split(",")
        MAVEN_COMMON_ERRORS_MAP[exception] = action

GRADLE_COMMON_ERRORS = []
with open('/home/notebooks/ProjectAnalysis/GitHubProyectsAnalysis/gradle-common-errors.txt', "r") as f:
    for line in f.readlines():
        exception, action = line.rstrip("\n").split(",")
        GRADLE_COMMON_ERRORS.append((exception, action))

ANT_COMMON_ERRORS = []
with open('/home/notebooks/ProjectAnalysis/GitHubProyectsAnalysis/ant-common-errors.txt', "r") as f:
    for line in f.readlines():
        exception, action = line.rstrip("\n").split(",")
        ANT_COMMON_ERRORS.append((exception, action))

HEADERS = ["INDEX","COMMIT_ID","BUILD_SYSTEM","BUILD_STATUS","ERROR", "ACTION"]

class LogAnalyzerGitHub:
    

    def __init__(self, project_name, root="../results/", experiment=1):
        self.project = project_name
        self.path= "%s/%s/experiment_%d"%(root, project_name, experiment)
        self.logs_path = self.path+'/logs/'
        report="%s/report_experiment_%d.csv"%(self.path, experiment)
        data= pd.read_csv(report)
        self.csvList = dict()
        with open(report) as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader):
                self.csvList[idx] = row
    
    def get_build_file(self, idx, commit_hash):
        build_file_path=self.path+"/build_files/%d-%s-build.json"%(idx, commit_hash)
        with open(build_file_path) as f: 
            data = json.load(f)
            return data

    def get_maven_errors(self, log_path):
        detectedErrors = []
        last_lines = subprocess.check_output(['cat', self.logs_path+log_path])
        for error in MAVEN_COMMON_ERRORS_MAP.keys():
            if error in str(last_lines):
                detectedErrors.append(error)
        return detectedErrors


    def get_error(self, build_system, commit_id, commit_hash):
        # First log Only ( Maven > Gradle > Ant )
        log_path = "%s-%s-attempt-1.log" % (commit_id, commit_hash)
        log = str(subprocess.check_output(['cat', self.logs_path+log_path])).replace("\\'", "'")

        # MAVEN

        if build_system == "Maven":
            for error in MAVEN_COMMON_ERRORS_MAP.keys():
                if error in log:
                    return error, MAVEN_COMMON_ERRORS_MAP[error]
            return "Other Maven error", "Other"
            #print("%d - Other Maven error" % commit_id)

        # GRADLE

        if build_system == "Gradle":
            for error in GRADLE_COMMON_ERRORS:
                if error[0] in log:
                    return error[0], error[1]
            #print("%d - Other Gradle error" % commit_id)
            return "Other Gradle error", "Other"

        # ANT 

        if build_system == "Ant":
            for error in ANT_COMMON_ERRORS:
                if error[0] in log:
                    return error[0], error[1]
            #print("%d - Other Ant error" % commit_id)
            return "Other Ant error", "Other"
        if build_system == "NOT_FOUND":
            return "No build system detected", "-"

        return "NO_VALID_BUILD_SYSTEM", "-"

    def analyze(self):

        # Create results folder (if not exist)
        analyze_results_path = "results/"
        if not os.path.exists(analyze_results_path):
            os.mkdir(analyze_results_path)

        results = []

        result_path = analyze_results_path + self.project + '.csv'
        if os.path.exists(result_path):
            print("> Project %s already analyzed"%self.project)
            return

        for idx in self.csvList:

            project = self.csvList[idx]

            build_file = self.get_build_file(idx, project['commit'])
            build_system = build_file['build_system']
            error = ""
            action = ""
            if project['build'] != "SUCCESS":
                if int(project['exec_time']) >= 300:
                    error = "Timeout"
                else:
                    error, action = self.get_error(build_system, idx, project['commit'])

            results.append({
                "INDEX": idx,
                "COMMIT_ID": project['commit'],
                "BUILD_SYSTEM": build_system,
                "BUILD_STATUS": project['build'],
                "ERROR": error,
                "ACTION": action
            })

        # SAVE RESULTS
        with open(analyze_results_path + self.project + '.csv', 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(results)
        
        print("> Project %s analyzed" % self.project)
        

if __name__ == "__main__":
    la = LogAnalyzerGitHub('mockito', root="/home/results/GitHub_old/")
    la.analyze()

    # from os import listdir
    # from os.path import isfile, join

    # from collections import Counter

    # projects = [f for f in listdir("/home/results/GitHub/")]

    # build_systems = []

    # for project in projects:
    #     path = join("/home/results/GitHub/", project)
    #     build_path = join(path, "experiment_1/build_files/")
    #     for build_file in listdir(build_path):
    #         with open(join(build_path, build_file)) as f:
    #             bs = json.load(f)
    #             build_systems.append((bs['build_system']))
    # print(Counter(build_systems))
    
    # Counter({'Maven': 83951, 'Ant': 15227, 'Gradle': 11416, 'NOT_FOUND': 4518})

    

