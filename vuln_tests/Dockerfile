FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
CMD ["python", "-m", "vuln_tests.tests.test_runner"]
