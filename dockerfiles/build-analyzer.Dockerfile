# Pull base image.
FROM python:3.7

# Install Docker

RUN curl -fsSL https://get.docker.com | sh

RUN pip install --upgrade pip
ADD py/requirements.txt requirements.txt
RUN pip install -r requirements.txt

VOLUME ["/home/bugs/projects/"]

RUN echo "PS1='\[\033[1;36m\]BuildAnalycer \[\033[1;34m\]\w\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> ~root/.bashrc

WORKDIR /home/bugs/

CMD ["bash"]
# BUILD docker build -f dockerfiles/build-analyzer.Dockerfile -t  maes95/build-analyzer:0.3.1-dev .
# RUN   docker run -it -p 8888:8888 -v $PWD/analysis:/home/bugs/analysis -v $PWD/py:/home/bugs/py -v $PWD/configFiles:/home/bugs/configFiles -v /var/run/docker.sock:/var/run/docker.sock --privileged=true build-analyzer:0.2-dev