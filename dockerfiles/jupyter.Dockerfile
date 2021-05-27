FROM playniuniu/jupyter-pandas

RUN pip install --upgrade pip
# ENV PIP_PACKAGE pandas pandas-datareader
# RUN pip install ${PIP_PACKAGE}

RUN apk add --no-cache git

WORKDIR /home/notebooks/

CMD ["jupyter-notebook", "--notebook-dir=/home", "--ip='0.0.0.0'", "--port=8888","--NotebookApp.token=''","--allow-root"]

# BUILD docker build -f dockerfiles/jupyter.Dockerfile -t jupyter-bugs .
# RUN docker run -d --rm --name jupyter-bugs -p 8888:8888 -v $PWD:/home/ -w /home/ jupyter-bugs