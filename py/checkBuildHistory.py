# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import datetime
import time
import csv
import json
import pickle
import json
from time import gmtime, strftime
from javaBuildHelper import JavaBuildHelper
from utils import ProcessManager, GitManager, DockerManager, DELIMITER

class BuildChecker():

    HEADERS = ["id", "commit", "build", "exec_time", "date", "comment"]

    def __init__(self, config_file_path, test=False):

        with open(config_file_path) as config_file:
            self.config = json.load(config_file)
        self.config['experiment'] = int(self.config['experiment'])
        self.firstTime = False
        self.test = test
        self.config['last_commit'] = self.config['last_commit'][0:8]
        
        # PATHS
        self.root = os.getcwd()
        self.path = '%s/results/%s/experiment_%s/'%(self.root, self.config['project'], self.config['experiment'])
        self.build_files_path = "%s/build_files/"%(self.path)
        self.logs_path = "%s/logs/"%(self.path)
        self.general_logs_path = "%s/general_logs/"%(self.path)
        self.out_report = "%s/report_experiment_%d.csv"%(self.path,self.config['experiment'])
        self.project_folder = "projects/%s" % self.config['project']

        # GET PROYECT (IF NOT EXIST IN LOCAL FOLDER /projects)
        if not os.path.isdir(self.project_folder):
            if not 'git_url' in self.config:
                raise Exception("Project does not exist and 'git_url' param not provided in config file")
            else:
                print("Project '%s' not available locally. Downloading ..."%self.config['project'])
                ProcessManager.default_exec("git clone %s %s"%(self.config['git_url'], self.project_folder))

        if not os.path.isdir(self.path):
            # FIRST EXECUTION
            self.firstTime = True
            os.makedirs(self.logs_path)
            os.makedirs(self.general_logs_path)
            os.makedirs(self.build_files_path)
        
        self.process_manager = ProcessManager(open(self.general_logs_path+"general-"+strftime("%d%b%Y_%X", gmtime())+".log", 'w+'), "BUILD CHECKER")
        self.git_manager = GitManager(self.process_manager, self.config['last_commit'])
        self.docker_manager = DockerManager(self.process_manager)
        
        if self.firstTime:
            # FIRST EXECUTION
            self.createCSVFile()

        # READ LAST REPORT
        with open(self.out_report) as csvfile:
            reader = csv.DictReader(csvfile)
            self.csvDict = dict()
            for row in reader:
                self.csvDict[row['commit']] = row
            # SORT ITEMS BY ID (DON'T NEED IT IN PYTHON 3.6)
            self.csvItems = sorted(self.csvDict.items(), key=lambda tup: int(tup[1]['id']) )
            # Set number of builds to total builds 
            if not 'number_of_builds' in self.config or self.config['number_of_builds'] == "All":
                self.config['number_of_builds'] = len(self.csvItems)

        # MOVE TO PROJECT
        os.chdir(self.project_folder)
       

    def checkBuild(self):

        self.process_manager.log("CHECK BUILD FOR EXPERIMENT %d" % self.config['experiment'])
        n = self.config['number_of_builds']
        count = 0
        total = n
        build_config = self.config.get('build_config')
        for c_hash, commit in self.csvItems:

            count = count + 1

            if (commit['build'] == "NO"):

                # NO BUILD CHECKED

                build_config = self.buildProject(c_hash, commit, build_config)

                # SAVE BUILD FILE

                self.saveBuildFile(commit, c_hash, build_config)

                n-=1
                if n == 0: break
            
            else:

                # BUILD CHECKED
                
                if commit['build'] == "SUCCESS":
                    self.process_manager.log("%s commit already checked: SUCCESS" % c_hash)
                if commit['build'] == "FAIL":
                    self.process_manager.log("%s commit already checked: FAIL" % c_hash)
            
            if not self.test:
                print("Builds checked : "+str(count)+"/"+str(total), end="\r")

    def buildProject(self, c_hash, commit, build_config, i = 1):

        self.process_manager.log("%s commit gona be checked" % c_hash)

        bh = JavaBuildHelper(self.process_manager)

        # GO TO  COMMIT 
        self.git_manager.change_commit(c_hash)

        # PATH WHERE LOG WILL BE STORE
        log_file_template = self.logs_path+str(commit['id'])+"-"+c_hash+"-attempt-%d.log"

        if 'build_config' in self.config:
            build_configs = [self.config['build_config']]
        else:
            build_configs = bh.getBuildConfigs(build_config)
        
        delta_time = 0

        for idx, bc in enumerate(build_configs):
            
            start = round(time.time())
            # Start build
            exit_code = bh.executeBuildSystem(self.config["project"],self.docker_manager, bc, log_file_template%(idx+1))
            # End build
            delta_time = round(time.time()) - start

            if exit_code == 0:
                # SUCCESS
                self.process_manager.log("%s commit build success" % c_hash)
                commit['build'] = "SUCCESS"
                commit['exec_time'] = delta_time
                bc["works"] = True
                bc = bc.copy()
                bc["builds_checked"] = build_configs
                self.updateFile()
                return bc
        
        # NO BUILD WORKS 
        self.process_manager.log("%s commit build fail" % c_hash)
        commit['build'] = "FAIL"
        commit['exec_time'] = delta_time
        # RETURN FIRST BUILD CONFIG DETECTED, RETURN ALL BUILDS AS A PARAM
        bc = build_configs[0].copy()
        bc["builds_checked"] = build_configs
        self.updateFile()
        return bc    

    def saveBuildFile(self, commit, c_hash, build_config):
        filename = str(commit['id'])+"-"+c_hash+"-build.json"
        with open(self.build_files_path+filename,'w+') as json_file:
            data = {
                "commit": c_hash,
                "build_system": build_config["build_system"],
                "docker_image": build_config["docker_image"],
                "build_command": build_config["build_command"],
                "build_file": build_config["build_file"],
                "builds_checked": build_config["builds_checked"],
                "works": commit['build'] == "SUCCESS"
            }
            json.dump(data, json_file, indent=4)

            

    def createCSVFile(self):
        # GO PROJECT FOLDER
        os.chdir(self.project_folder)
        with open(self.out_report, 'w+') as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames = self.HEADERS) 
            commits = []
            n=0
            rawCommits = []
            if 'commits' in self.config:
                rawCommits = [(commit["c_hash"], commit['date'], commit['comment']) for commit in self.config['commits']]
            else:
                rawCommits = [ commit.split(DELIMITER) for commit in self.git_manager.getAllCommits()]

            for commit in rawCommits:
                commit_hash, date, comment = commit
                commits.append({
                    "id": n,
                    "commit": commit_hash[0:8],
                    "build": "NO",
                    "exec_time": 0,
                    "date": date,
                    "comment": comment
                })
                n+=1
            writer.writeheader()
            writer.writerows(commits)
        # GO BACK
        os.chdir(self.root)

    def updateFile(self):
        with open(self.out_report, 'w+') as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames = self.HEADERS) 
            writer.writeheader()
            for _, commit in self.csvItems:
                writer.writerow(commit)
    
    def finish(self, msg):
        # RESTORE STATE AND CLOSE FILES
        self.process_manager.log(msg)
        self.docker_manager.shutdownContainers()
        os.chdir(self.root)
        self.process_manager.execute("chmod -R ugo+rw %s/results/"%self.root)
        self.process_manager.close()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Use: python py/checkBuildHistory.py <config_file_path>")
        exit()

    bcheck = BuildChecker(sys.argv[1])

    try:
        bcheck.checkBuild()
    except KeyboardInterrupt as e:
        bcheck.finish("FINISHED EXPERIMENT WITH KeyboardInterrupt")
    except Exception as e:
        bcheck.pm.log("Exception: %s"%e)
        bcheck.finish("FINISHED EXPERIMENT WITH AN EXCEPTION")
    else:
        bcheck.finish("FINISHED EXPERIMENT SUCCESSFULLY")



