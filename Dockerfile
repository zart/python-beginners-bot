FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "main.py"]
