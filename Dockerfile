FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app

RUN apt-get update && apt-get install -y r-base && apt-get install -y gdal-bin
RUN Rscript -e "install.packages('remotes', dependencies=TRUE, upgrade=TRUE); if (!library(remotes, logical.return=T)) quit(status=10)"
RUN Rscript -e "remotes::install_github('rdotsch/rcicr', dependencies=TRUE, upgrade=TRUE); if (!library(rcicr, logical.return=T)) quit(status=10)"
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5001"]