FROM centos/python-36-centos7
MAINTAINER Sreekanth Kocharlakota (sreekanth.kocharlako@247.ai)
LABEL Vendor="Github Spyder" \
      Version=1.0-0
WORKDIR /root
RUN pip install scrapy
RUN pip install pyyaml
RUN pip install ujson
COPY input.yml .
COPY main.py .
COPY github-scraper.py .
ENTRYPOINT ["python", "main.py" ]
