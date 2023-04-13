[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5596333.svg)](https://doi.org/10.5281/zenodo.5596333)
# Reproducing open-projects software builds experiment

> This repository constitutes the reproduction package of Chapter 3 of the PhD. Thesis titled `Hunting Bugs: A study of the change history of open-source software projects and its application to the detection of how these changes introduce bugs`, written by Michel Maes Bermejo. This repository is a fork of the repository that contained the original reproduction package published in Empirical Software Engineering (to avoid altering it for preservation).

Reproduction package for the paper "Back and There Once Again: Revisiting the Compilation of Past Snapshots", published at Empirical Software Engineering in 2022.

DOI of Publication: [https://doi.org/10.1007/s10664-022-10117-6](https://doi.org/10.1007/s10664-022-10117-6)

This package contains:

```bash
.
├── configFiles     # Config files for each project
├── dockerfiles     # Docker files for all necessary images to perform the experiment
├── notebooks       # Jupyter Notebooks for data extraction and analysis
├── previousResults # Results from Original Study
├── projects        # Subjects of the experiment (git repositories)
├── py              # Python scripts to perform the experiment
├── results         # Contains the results generate from the experiment
├── scripts         # Bash scripts to easy-perform the experiment
├── tmp             # Folder for temporary files
└── README.md 
```

In addition, the rest of this file describe methodological details of the studies presented in the paper, and provides an introduction to the data:

- [Original Study](#original-study) -> Summary of the previous experiment leading to ours and its results
- [Set Up](#set-up) -> Technical requirements to reproduce the experiments
- [Replication Study](#replication-study)
    - [Step 1: Project Mining](#step-1-project-mining-replication-study)
    - [Step 2. Buildability experiment](#step-2-buildability-experiment-replication-study)
    - [Step 3. Results analysis](#step-3-results-analysis-replication-study)
- [Reproduction Study](#reproduction-study)
    - [Step 1: Project Mining](#step-1-project-mining-reproduction-study)
    - [Step 2. Buildability experiment](#step-2-buildability-experiment-reproduction-study)
    - [Step 3. Results analysis](#step-3-results-analysis-reproduction-study)

Some data needed to correctly reproduce the experiment is hosted in Zenodo (https://zenodo.org/record/5596333), due to the limitations of the GitHub file size (the size of the dataset >250GB). The dataset hosted in Zenodo contains the following zip files:

- ApacheProjects.zip
- ApacheProjects-SoftwareHeritage.zip
- GitHubProjects.zip
- ReplicationResults.zip
- ReproductionResults.zip

The use of these datasets will be discussed in the following sections.

> **IMPORTANT NOTE**: In this reproduction package, the term "buildability" is used equivalently to the term "compilability".

## Original study

Our work is the continuation of a previous work that we will call _Original Study_, an experiment carried out by Tufano et al. in their publication Tufano et al. in their publication: [There and back again: Can you compile that snapshot?](https://doi.org/10.1002/smr.1838). A data [reproducilibity package](http://www.cs.wm.edu/semeru/data/breaking-changes/) for that paper is public available


In the Original Study, the study of the compilability of the snapshots (commits) of 100 Apache projects (Java) was addressed. Their procedure is as follows:

1. Select a project
2. Go over the commit history of the project (master branch)
3. A commit is selected
4. Check that a pom.xml file exists.
5. A compilation is performed using the Maven library from Java (only if the pom.xml file exists)
6. Get the status of the build (0 or!0) and the reason for the failure (an exception thrown by Maven).
7. A record is kept in the results table (see Table 1)
8. Go to the next commit an repeat steps 3-7

Based on the results obtained, they aim to answer the following RQs:

- RQ1: _“How many snapshots are currently compilable in the change history?”_
- RQ2: _“Which types of errors can be observed by automatically compiling code snapshots?”_

##### Results

On average, only 38% of the snapshots are compilable. The main problem encountered is the resolution of dependencies, and the compilability results and failure reasons associated with each project.

They get the failure reason by capturing exceptions during the build (they use a Java library to build the snapshots).

## Set Up

*Pre-requisites to reproduce our work*

- Git 2.17+
- Docker 19+

These dependencies will be needed to download this repository, build the Docker images and run the containers from those images.

First of all, clone the repo:

```
  $ git clone https://github.com/BuildabilityResearcher/BuildabilityStudy.git
  $ cd bugs/
```

## Replication Study

This section details the steps taken to replicate Original Study using the original projects.

### Step 1. Project mining - Replication Study

##### 1.1 Download Repositories

The Apache projects recovered in the Original Study had been obtained from GitHub. 

> From the 100 projects studied::
> - 94 have been successfully downloaded
> - 6 projects no longer exist in GitHub. The projects have been deleted, archived or renamed (Table 1)

##### 1.2 Explore commit history

From the Apache projects obtained from GitHub (94) we have checked if the commits collected in the results of the Original Study are still available in the historical one. This is because it is possible that the commits have disappeared. Most commonly this is because of the following reasons:

- The local repository is outdated.
- The branch containing the commit was removed, so the commit is no longer referenced.
- Someone forced the push on the commit.

To do this, we check that each of the commits defined in the results above exists.

> From the 94 projects recovered:
> - 19 repositories NOT contain all the defined commits (Table 2)
>   - 8 do not contain any of the defined commits
>   - 11 repositories have SOME commits (0.14%-99.4%)
> - 75 repositories have ALL available commits.

*Table 1: Projects we failed to recover from github (6 projects)*

|                Project |
|-----------------------:|
|                 visper |
| myfaces-portlet-bridge |
|      webservices-axion |
|  webservices-xmlschema |
|                  wss4j |
|     webservices-neethi |

*Table 2: Proyects recovered from GitHub without all their commits (19 projects)* 

|              Project | Commits Recovered | Not Recovered  | Total Commits | % Recovered |
|---------------------:|------------------:|-----:|--------------:|------------:|
|       myfaces-extcdi |               167 |    1 |           168 |       99,40 |
|              opennlp |                19 | 1209 |          1228 |       15,47 |
|           jackrabbit |               547 | 7451 |          7998 |       68,39 |
|            uima-ducc |              1783 |  644 |          2427 |       73,47 |
|                 tika |               386 | 1866 |          2252 |       17,14 |
|       santuario-java |                 0 |  579 |           579 |        0,00 |
|                  sis |                 5 |  394 |           399 |       12,53 |
|           manifoldcf |              1938 |  480 |          2418 |       80,15 |
| jackrabbit-filevault |                49 |   75 |           124 |       39,52 |
|              streams |                 0 |   69 |            69 |        0,00 |
|       jackrabbit-ocm |                37 |  358 |           395 |        9,37 |
|              myfaces |                 0 | 2367 |          2368 |        0,00 |
|         james-mailet |                 0 |   66 |            66 |        0,00 |
|           james-imap |                 0 | 1100 |          1100 |        0,00 |
|                shiro |                 1 |  687 |           688 |        0,15 |
|      maven-archetype |                 0 |  826 |           826 |        0,00 |
|       jackrabbit-oak |                41 | 7804 |          7845 |        0,52 |
|        james-mailbox |                 0 |  614 |           614 |        0,00 |
|      james-protocols |                 0 |  591 |           591 |        0,00 |

##### 1.3 Recovery of projects from Software Heritage 

From the 25 discarded projects, 6 do not exist in GitHub and 19 of them are missing at least 1 snapshot that was analyzed in the Original Study.

To try to replicate the experiment more completely, we use the [Software Heritage](https://www.softwareheritage.org/) online tool.

Software Heritage is an initiative to collect, preserve and share software code in a universal software archive. From its online platform it is possible to recover repositories that were saved in the past and are no longer in their original source.

The repositories are obtained semi-automatically, you need to search the repository and ask the tool to generate a git repository from the snapshots it has stored of that project (quite a slow process).

> All repositories have been found in Software Heritage:
> - 5 of them could not be downloaded (Table 3)
>   - 3 of them were empty (nothing can be recovered).
>   - 2 of them are corrupt (they give a 504 error after several attempts).
> - 20 of them have been downloaded and explored again (Table 4)
>   - 4 of them contain all the commits made in the Original Study and are added to the 75 previously obtained
>   - 16 of them do not contain all the commits made in the Original Study and are discarded definitively.

*Table 3: Projects that could not be recovered from Software Heritage* 

|               Project |                                      Error |
|----------------------:|-------------------------------------------:|
| webservices-xmlschema | Internal Server Error in Software Heritage |
|          james-mailet |       Empty repository                     |
|        jackrabbit-oak | Internal Server Error in Software Heritage |
|         james-mailbox |       Empty repository                     |
|       james-protocols |       Empty repository                     |

*Table 4: Results of trying to recover projects from Software Heritage* 

|                Project | Commits Recovered | Not Recovered | Total Commits | % Recovered |
|-----------------------:|------------------:|--------------:|--------------:|------------:|
|                *visper*|               678 |             0 |           678 |      100,00 |
| *myfaces-portlet-bridge* |                27 |             0 |            27 |      100,00 |
|      webservices-axion |                 0 |          2790 |          2790 |        0,00 |
|                  *wss4j* |              1943 |             0 |          1943 |      100,00 |
|     *webservices-neethi* |               358 |             0 |           358 |      100,00 |
|         myfaces-extcdi |               167 |             1 |           168 |       99,40 |
|                opennlp |                19 |          1209 |          1228 |       15,47 |
|             jackrabbit |                 0 |          7998 |          7998 |        0,00 |
|              uima-ducc |              1783 |           644 |          2427 |       73,47 |
|                   tika |                 0 |          2252 |          2252 |        0,00 |
|         santuario-java |                 0 |           579 |           579 |        0,00 |
|                    sis |                 5 |           394 |           399 |       12,53 |
|             manifoldcf |              1938 |           480 |          2418 |       80,15 |
|   jackrabbit-filevault |                 0 |           124 |           124 |        0,00 |
|                streams |                 0 |            69 |            69 |        0,00 |
|         jackrabbit-ocm |                 0 |           395 |           395 |        0,00 |
|                myfaces |                 0 |          2367 |          2368 |        0,00 |
|             james-imap |                 0 |          1100 |          1100 |        0,00 |
|                  shiro |                 1 |           687 |           688 |        0,15 |
|        maven-archetype |                 0 |           826 |           826 |        0,00 |

##### 1.4 Generate build configuration files

For each of the projects that have all their commits (79) a configuration file is generated in order to perform the snapshot compilation experiment.

The configuration file follows this structure:

```json
{
   "project": "isis",
   "git_url": "https://github.com/apache/isis.git",
   "last_commit": "5a252cbb",
   "experiment": 1,
   "commits": [
       {
           "c_hash": "ce17d076",
           "date": "2004-07-30 11:02:50 +0000",
           "comment": "initial checkin"
       }, // More commits ...
   ]
}

```

In the Original Study, a total of 219,395 snapshots were considered in 100 projects. In the replication experiment, we have recovered 139,389 snapshots from 79 projects (these projects have all their snapshots). Of the recovered snapshots, 136,383 have been recovered from GitHub (75 projects) and 3006 have been recovered from Software Heritage. From the snapshots recovered, 101,811 contain the _pom.xml_ configuration file and can be attempted to be built.

The 79 projects on which the Replication Experiment will be performed can be found in the `configFiles/ApacheProjects` folder

#### To execute this step

The execution of step 1 is implemented in a single Jupyter Notebook.

To reproduce this step:

- Build docker image Jupyter docker image locally
```
$ docker build -f dockerfiles/jupyter.Dockerfile -t jupyter-bugs .
```
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```
- [Open ApacheProjectsMining notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectsMining/ApacheProjectsMining/ApacheProjectsMining.ipynb)
- [Open ApacheProjectsMining notebook in Gitlab/GitHub](notebooks/ProjectsMining/ApacheProjectsMining/ApacheProjectsMining.ipynb)

INPUT: 
- Info from Original Study projects: `previousResults/analyzedProjects/`

OUTPUT: 
- Folder `configFiles/ApacheProjects/` which contains all config files for next step
- All Apache projects downloaded from GitHub at folder: `projects/`

> **Notes:**
> - Execute this experiment (download and analyze repositories) takes a considerable amount of time. *Pickle* files will be generated as intermediate files, which storage to re-execute only certain cells of notebook if needed.
> - If a pickle file is generated, re-execute this project only print a message.
> - If order to be able to reproduce the experiment, the following files and folders are provided:
>   - Pickle files (notebooks/ProjectsMining/ApacheProjectsMining/results/)
>   - Git repositories from GitHub (`ApacheProjects.zip`, available in [Zenodo dataset](https://zenodo.org/record/4002023))
>   - Git repositories from Software Heritage (`ApacheProjects-SoftwareHeritage.zip`, available in [Zenodo dataset](https://zenodo.org/record/4002023))
>   - Config files at `configFiles/ApacheProjects/`


### Step 2. Buildability experiment - Replication Study

##### 2.1 Experiment process

From the configuration files generated in the previous step (Step 1), the defined commits/snapshots will be built iteratively for each project:

1. The repository is downloaded (if it does not available locally)
2. Inside the repository, it is placed in the commit you want to check
3. The build command for Maven is executed (mvn clean compile -X) inside a Docker container.
4. The success code (0 or not 0) and the log are collected (the verbose option of the command is used to obtain the most detailed log)
5. Repeat steps 2-4 for the next commit.

##### 2.2 Experiment Results

For each project, a results folder is generated in the `results/` folder which the following content:

- `build_files/` A JSON file is stored in this folder for each commit that collects the tested build settings and their result (whether it worked or not)
- `general_logs/` This folder contains a general log of the execution of the experiment. If this experiment was paused and resumed later, a new log is generated.
- `logs/` This folder stores a log for each build configuration executed on a snapshot.
- `report_experiment.csv` This file contains the information of the results of the experiment. For each commit, it specifies whether it was successfully built or not, the execution time required by the build, and additional information about the snapshot, such as its creation date or the comment associated with the commit (See Table 5). 

*Table 5: Commit report example* 

| ID |  COMMIT  | BUILD |  EXEC_TIME |      DATE      |     COMMENT    |
|----|----------|-------|------------|----------------|----------------|
| 0  | 7d7bd006 | FAIL  | 2004-02-06 | 15:08:17 +0000 | Initial Layout |

##### 2.3 Differences from the Original Study

The main differences from the Original Study are as follows:
- Instead of capturing the exceptions, we keep the entire execution log.
- Building settings are provided to easily replicate the experiment (using Docker images)

#### To execute this step

The execution of Step 2 is implemented as a Docker container.

To reproduce this step:

- Build docker image Jupyter docker image locally
```
$ docker build -f dockerfiles/build-analyzer.Dockerfile -t  build-analyzer .
```
- Run a docker container from this image (PWD should be root folder of the project). You need to set _<project_name>_ (i.e. `isis`) and _<path_to_config_file>_ (i.e. `configFiles/ApacheProjects/isis-config.json`)
```
$ docker run -d --rm\
    -v $PWD/results:/home/bugs/results \
    -v $PWD/py:/home/bugs/py \
    -v $PWD/projects:/home/bugs/projects \
    -v $PWD/configFiles:/home/bugs/configFiles \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -w /home/bugs/ \
    --name build-experiment-<project_name> \
    --privileged=true \
    build-analyzer python py/checkBuildHistory.py <path_to_config_file>
```

To make the execution easier, a bash script is provided to launch the experimentation of a project just from its name:  

```
$ ./scripts/runApacheExperiment.sh <project_name>
```

INPUT: 
- Configuration files from `configFiles/ApacheProjects/`

OUTPUT: 
- Folders in `results/` per project as defined in section 2.2.

> **Notes:**
> - Execute this experiment takes a considerable amount of time (~3 weeks depending of your machine). If order to be able to check the analysis, our results as provided as ZIP file `ReplicationResults.zip`, available in [Zenodo dataset](https://zenodo.org/record/4002023). The unzipped file size is 95GB.
> - Once you run the experiment or download the results (and unzip it), move the results files to a new directory (`results/Apache`) so that the other scripts know where to look.

### Step 3. Result Analysis - Replication Study

#### 3.1 Buildability Analysis - Replication Study

We will replicate the format of the compilability results used in the Original Study. The quartile values for the 79 projects are Q1=202.5 and Q3=1148 commits. The number of projects for each category would be 20 (short history), 39 (medium history) and 20 (long history)

We have calculated the compilability results of the Original Study together with the results of our experiment (Tables 6 and 7 respectively). The previous results have been calculated considering the compilability results of the 79 projects that we have been able to recover in order to make a fair comparison. The results obtained in the Original Study by reducing the number of projects are close to those presented in Tufano et al. work. For example, the average compilability of the projects in Table 6 is 37.19 while the average compilability provided in Tufano et al. paper is 38.13.

A summary of the results of buildability is provided in the following file: 
- _results/replication_experiment_buildability_summary.csv_

##### To execute this step

The execution of step 3.1 is implemented in Jupyter Notebook.

To reproduce this step:

- Build `jupyter-bugs` image if you have not previously built it (see Step 1)
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```
- Check the results using the following notebook [Open ApacheStatusChecker notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheStatusChecker.ipynb) or [Open ApacheStatusChecker notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheStatusChecker.ipynb)
    - INPUT:  Results placed in folder `results/Apache/`
    - OUTPUT: CSV file `ApacheStatusCheckerResults.csv` 
- Analyze the results in a deeper way [Open ApacheStatusAnalysis notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheStatusAnalysis.ipynb) or [Open ApacheStatusAnalysis notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheStatusAnalysis.ipynb)
    - INPUT: CSV file `ApacheStatusCheckerResults.csv`
    - OUTPUT: Tables (open notebook to see them in detail)

#### 3.2 Error Analysis - Replication Study

To answer this question, we extract the exception produced from the log for the failed builds. The exceptions that can be produced during the construction of the Maven project are [well defined and limited](https://cwiki.apache.org/confluence/display/MAVEN/Errors+and+Solutions)

We will use the classification and mapping of exceptions made by Tufano et al. (available in file `previousResults/maven-common-errors.txt`), who defined 4 categories: 
- Resolution errors
- Parsing errors 
- Compilation errors
- Other errors.

In addition to just counting the exceptions as in the Original Study, our aim is to make an exhaustive study of how these errors have changed. We have considered that the errors we have can be split into three categories:
- **New errors**: The previous build works, but a new error
appears that prevents built the snapshot successfullt now
- **Same error**: The buid fails for the same reason as before.
- **Different errors**: The build fails, but for a new cause

We also considered the possibility that there are snapshots that previously could not be built and now can be built.

##### To execute this step

The execution of step 3.2 is implemented in Jupyter Notebook.

To reproduce this step:

- Build `jupyter-bugs` image if you have not previously built it (see Step 1)
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```
- Check the results using the following notebook [Open ApacheLogChecker notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheLogChecker.ipynb) or [Open ApacheLogChecker notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheLogChecker.ipynb)
    - INPUT:  Results placed in folder `results/Apache/`
    - OUTPUT: Results per project in `notebooks/ProjectAnalysis/ApacheProyectsAnalysis/results/` folder  (CSV files)
- Analyze the results in a deeper way [Open ApacheLogAnalysis notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheLogAnalysis.ipynb) or [Open ApacheLogAnalysis notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/ApacheProyectsAnalysis/ApacheLogAnalysis.ipynb)
    - INPUT: Results per project from `notebooks/ProjectAnalysis/ApacheProyectsAnalysis/results/` folder (CSV files)
    - OUTPUT: Tables (open notebook to see them in detail)

## Reproduction Study

This section details the steps taken to reproduce Tufano et al.'s study using new projects

### Step 1. Project mining - Reproduction Study

To perform the reproduction of the study, it is necessary to generate a new project dataset. For this purpose, a search has been performed using the GitHub API with the following parameters:

- Only Java projects are allowed
- Have at least 500 stars and 300 forks
- They've had at least five years of development
- Are currently in development

The exact query was:

```
    language:java 
    stars:>=500 
    forks:>=300 
    created:<2015-01-01 
    pushed:>2020-01-01
    archived:false
    is:public
```

Information has been obtained and stored from a total of 682 projects.

On this dataset, a number of conditions have been applied to reduce their number.

##### Condition 1: Build System

Although it is most common for projects to have a construction system, we need to make sure that those we download use one of the main build systems (Maven, Gradle or Ant). To do this, we check that in their most recent commit they have a pom.xml, build.gradle or build.xml file respectively.

> OUTPUT: 596 projects

##### Condition 2: Commit range

We want to set a lower limit of 1,000 commits to avoid getting projects that have been resubmitted or have an insufficient number of commits to make sense of analyzing their history.

The upper limit has been set at 10,000 to avoid projects with too large a history, which can lead to time-consuming experimentation.

> OUTPUT: 298 projects

##### Condition 3: Android projects

Among the other projects, it is possible that we find Android libraries or applications. Their built is limited as they need specific SDKs so we have decided to discard them. To do this, we check the build.gradle file for Android libraries.

> OUTPUT: 252 projects

##### Random selection

From the 252 projects that meet our requirements, we have chosen a random sample of 80 projects.

##### Generate build configuration files

For each of these 80 projects, a configuration file is generated in order to perform the snapshot compilation experiment

The configuration file is quite similar to the Original Study, but in this case, we consider the entire commit history down to the most recently defined commit:

```
{
    "project": "assertj-core",
    "git_url": "https://github.com/joel-costigliola/assertj-core.git",
    "last_commit": "fc37b2d6",
    "experiment": 1
}
```

The 80 projects on which the Reproduction Experiment will be performed can be found in the `configFiles/GitHubProjects` folder

#### To execute this step

The execution of step 1 is implemented in a single Jupyter Notebook.

To reproduce this step:

- Build docker image Jupyter docker image locally (if not previously created)
```
$ docker build -f dockerfiles/jupyter.Dockerfile -t jupyter-bugs .
```
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```
- Open notebook:
    - [Open GitHubProjectsMining notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectsMining/GitHubProjectMining/GitHubProjectsMining.ipynb)
    - [Open GitHubProjectsMining notebook in Gitlab/GitHub](notebooks/ProjectsMining/GitHubProjectMining/GitHubProjectsMining.ipynb)

INPUT: 
- Nothing

OUTPUT: 
- Folder `configFiles/GitHubProjects/` which contains all config files for next step.
- All projects downloaded from GitHub at folder: `projects/`

> **Notes:**
> - If order to be able to reproduce the experiment, the following files and folders are provided:
>   - Pickle file (`notebooks/ProjectsMining/GitHubProjectMining/repos_backup.zip`). This pickle file contains data from 682 repositories obtained from GitHub.
>   - Config files at `configFiles/GitHubProjects/`
>   - Git repositories from GitHub (`GitHubProjects.zip`, available in [Zenodo dataset](https://zenodo.org/record/4002023))

### Step 2. Buildability experiment - Reproduction Study

The execution of the reproduction experiment is very similar to that of the replication experiment, except for the changes shown below:

- When we checkout a commit, the files are inspected for build files (Table 9). A build configuration is created for each build system found.

*Table 9: Build Options* 

| Build File              | Build System            | Build command           |
|-------------------------|-------------------------|-------------------------|
| pom.xml                 | Maven                   | mvn clean compile -X    |
| gradlew*                | Gradle                  | gradle compile          |
| build.xml               | Ant                     | ant compile -v          |

\* *__gradlew__ file is an executable, the build configuration is inferred and assumed to be in the same directory (build.gradle)*

_Example of build configuration_
```
{
    "build_system": "Maven",
    "docker_image": "java-maven-ant:0.1",
    "build_command": "mvn clean compile -X",
    "build_file": "pom.xml",
}
```

- When a build is performed, the build command defined in the build configuration are executed. 
- If the build fails and more than one build system has been detected, it is tested with the next one. The order of preference of the building systems is Maven > Gradle > Ant.

> **Notes:**
> - Execute this experiment takes a considerable amount of time (~5 weeks depending of your machine). If order to be able to check the analysis, our results as provided as ZIP file `ReproductionResults.zip`, available in [Zenodo dataset](https://zenodo.org/record/4002023). The unzipped file size is 155GB.
> - Once you run the experiment or download the results (and unzip it), move the results files to a new directory (`results/GitHub`) so that the other scripts know where to look.

### Step 3. Results analysis - Reproduction Study

#### 3.1 Buildability analysis - Reproduction Study

We will replicate the format of the compilability results used in the Original Study. The quartile values for the 37 projects are Q1=1791 and Q3=3693 commits. The number of projects for each category would be 20 (short history), 40 (medium history) and 20 (long history).

A summary of the results of buildability is provided in the following file: 
- _results/reproduction_experiment_buildability_summary.csv_

#### To execute this step

The execution of step 3.1 is implemented in a single Jupyter Notebook.

To reproduce this step:

- Build docker image Jupyter docker image locally (if not previously created)
```
$ docker build -f dockerfiles/jupyter.Dockerfile -t jupyter-bugs .
```
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```

- Check the results using the following notebook [Open GitHubStatusChecker notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubStatusChecker.ipynb) or [Open GitHubStatusChecker notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubStatusChecker.ipynb)
    - INPUT:  Results placed in folder `results/Apache/`
    - OUTPUT: CSV file `GitHubStatusCheckerResults.csv`
- Analyze the results using the following notebook [Open GitHubStatusChecker notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubStatusAnalysis.ipynb) or [Open GitHubStatusChecker notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubStatusAnalysis.ipynb)
    - INPUT: CSV file `GitHubStatusCheckerResults.csv`
    - OUTPUT: Tables (open notebook to see them in detail)

#### 3.2 Error Analysis - Reproduction Study

We extract the exception or error trace produced from the log for the failed builds. A different strategy has been followed for each build system:

- For the **Maven** projects, the same procedure has been used as in the replication experiment; use the exceptions launched by Maven.
- For the **Gradle** and **Ant** projects, we have tried to find the log trace that describes why it has not been possible to build the build. In some cases it is an exception, in others a specific message (i.e. _Could not resolve all dependencies_)

We will reuse the classification used in the replication experiment:

- Resolution errors
- Parsing errors
- Compilation errors
- Other errors.

The mapping from Exception/Log Trace to the previous clasification is available in the following files:

- Maven: `previousResults/maven-common-errors.txt`
- Gradle: `notebooks/ProjectAnalysis/GitHubProyectsAnalysis/ant-common-errors.txt`
- Ant: `notebooks/ProjectAnalysis/GitHubProyectsAnalysis/gradle-common-errors.txt`

#### To execute this step

The execution of step 3.2 is implemented in Jupyter Notebook.

To reproduce this step:

- Build `jupyter-bugs` image if you have not previously built it (see Step 1)
- Run a docker container from this image (PWD should be root folder of the project)
```
$ docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs
```
- Check the results using the following notebook [Open GitHubLogChecker notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubLogChecker.ipynb) or [Open GitHubLogChecker notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubLogChecker.ipynb)
    - INPUT:  Results placed in folder `results/GitHub/`
    - OUTPUT: Results per project in `notebooks/ProjectAnalysis/GitHubProyectsAnalysis/results/` folder  (CSV files)
- Analyze the results in a deeper way [Open GitHubLogAnalysis notebook in browser](http://localhost:8888/notebooks/notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubLogAnalysis.ipynb) or [Open GitHubLogAnalysis notebook in Gitlab/GitHub](notebooks/ProjectAnalysis/GitHubProyectsAnalysis/GitHubLogAnalysis.ipynb)
    - INPUT: Results per project from `notebooks/ProjectAnalysis/GitHubProyectsAnalysis/results/` folder (CSV files)
    - OUTPUT: Tables (open notebook to see them in detail)

