FROM python:3
ADD main.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
WORKDIR ./
CMD python main.py