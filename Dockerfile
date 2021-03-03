FROM continuumio/miniconda:latest
WORKDIR /HON_full

# conda env
COPY HON_env.yml ./
RUN conda env create -f HON_env.yml
RUN echo "source activate HON-env"
ENV PATH /opt/conda/envs/HON-env/bin:$PATH

# app folders with APP, tests ....
COPY HON ./HON
COPY wsgi.py ./
COPY config.py ./config.py
ENV FLASK_APP=HON

# initilize db
#RUN mkdir instance
RUN flask init-db

# start app
CMD ["gunicorn","--bind","0.0.0.0:5000","wsgi:app"]

