FROM ubuntu:22.04
RUN apt-get update && apt-get upgrade && apt-get install gcc g++ -y
WORKDIR ./work_dir/

ARG compiler=g++
ARG lang=cpp
ARG task_id=1
ARG problem_id=123
ARG filename=main.cpp
COPY ../data/works/$task_id/$filename ./
COPY ../data/tests/$problem_id/tests.$lang ./
COPY ../scripts/${lang} ./
RUN chmod +x $lang
ENV point=./$lang
ENTRYPOINT $point
