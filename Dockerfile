FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN useradd --shell /bin/false --create-home appuser
WORKDIR /home/appuser

COPY requirements.txt /tmp
RUN pip install --trusted-host pypi.python.org -r /tmp/requirements.txt && rm -rf /root/.cache/* && rm /tmp/requirements.txt

COPY . /home/appuser

CMD ["python", "main.py"]
