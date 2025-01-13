FROM python:3.13-slim-bullseye

WORKDIR /receipt-api
COPY requirements.txt .
COPY api.py .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["api.py"]