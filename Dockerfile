FROM python:3-11-slim
WORKDIR /root
COPY FetchEmail.py /root/
COPY main.py /root/
COPY requirements.txt /root/
RUN pip install -r /root/requirements.txt
CMD ["python3","/root/main.py"]