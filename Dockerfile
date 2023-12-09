FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y r-base
RUN apt-get install -y libpq-dev && apt-get install -y gdal-bin && apt-get install -y libgdal-dev

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN Rscript -e "install.packages('remotes', dependencies=TRUE, upgrade=TRUE); if (!library(remotes, logical.return=T)) quit(status=10)"
RUN Rscript -e "remotes::install_github('rdotsch/rcicr', dependencies=TRUE, upgrade=TRUE); if (!library(rcicr, logical.return=T)) quit(status=10)"

COPY . /app

CMD ["gunicorn", "-w 4", "app:app", "--bind 0.0.0.0:$PORT"]