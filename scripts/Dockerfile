FROM ubuntu:22.04
RUN apt-get update && apt-get upgrade && apt-get install gcc g++ -y
WORKDIR ./work_dir/

ARG compiler=g++
ARG lang=cpp
ARG task_id=123
ARG problem_id=123
COPY ./autolab/works/$task_id/$filename ./
COPY ./autolab/tests/$problem_id/tests.$lang ./
COPY ./autolab/scripts/${lang} ./
RUN chmod +x $lang
ENV point=./$lang
ENTRYPOINT $point
