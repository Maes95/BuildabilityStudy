import csv
import pandas as pd
import re
import hashlib
import os
import json
import subprocess

with open('/home/previousResults/maven-common-errors.txt', "r") as f:
    MAVEN_COMMON_ERRORS = [line.rstrip("\n").split(",")[0] for line in f.readlines()]

HEADERS = ["INDEX","COMMIT_ID","IS_MAVEN","OLD_BUILD_SUCCESSFUL", "NEW_BUILD_SUCCESSFUL", "OLD_EXCEPTION", "NEW_EXCEPTION"]

class LogAnalyzerApache:
    

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
        for error in MAVEN_COMMON_ERRORS:
            if error in str(last_lines):
                detectedErrors.append(error)
        return detectedErrors

    def analyze(self):

        # Create results folder (if not exist)
        analyze_results_path = "results/"
        if not os.path.exists(analyze_results_path):
            os.mkdir(analyze_results_path)

        results = []

        result_path = analyze_results_path + self.project + '.csv'
        # if os.path.exists(result_path):
        #     print("> Project %s already analyzed"%self.project)
        #     return

        with open("/home/previousResults/analyzedProjects/"+self.project+"/compilation.log.csv", 'r+') as f:
            reader = csv.DictReader(f, delimiter=",")
            for idx, old_result in enumerate(reader):

                # OLD: INDEX,COMMIT_ID,POM_FILE,BUILD_SUCCESSFUL,EXCEPTION,COMPONENT,ACTION
                # NEW: id,commit,build,exec_time,date,comment
                new_result = self.csvList[idx]

                build_file = self.get_build_file(int(new_result['id']), new_result['commit'])

                old_works = old_result['BUILD_SUCCESSFUL'] == 'true'
                
                # Get status only from Maven or no-build (ignore Ant)
                new_works = build_file['builds_checked'][0]['works']

                # Check build system
                isMaven = old_result['POM_FILE'] == 'true'

                if new_works and not isMaven: print("HEY")

                new_exceptions = []

                if not new_works:
                    # Only Maven log
                    log_path = "%s-%s-attempt-1.log" % (new_result['id'], new_result['commit'])
                    new_exceptions = self.get_maven_errors(log_path)

                    if len(new_exceptions)==0:
                        # Not Maven Exception captured
                        if int(new_result['exec_time']) >= 300:
                            # Timeout
                            new_exceptions.append("TIMEOUT")
                        else:
                            # Other
                            new_exceptions.append("OTHER")
                # RESULT: INDEX,COMMIT_ID,IS_MAVEN,OLD_BUILD_SUCCESSFUL, NEW_BUILD_SUCCESSFUL, OLD_EXCEPTION, NEW_EXCEPTION
                results.append({
                    "INDEX": idx, 
                    "COMMIT_ID": new_result['commit'], 
                    "IS_MAVEN": isMaven,
                    "OLD_BUILD_SUCCESSFUL": old_works,
                    "NEW_BUILD_SUCCESSFUL": new_works,
                    "OLD_EXCEPTION": old_result['EXCEPTION'],
                    "NEW_EXCEPTION": new_exceptions
                })

        # SAVE RESULTS
        with open(analyze_results_path + self.project + '.csv', 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(results)
        
        print("> Project %s analyzed" % self.project)
        

if __name__ == "__main__":
    la = LogAnalyzerApache('james-jsieve', root="/home/results/Apache_old/")
    la.analyze()
