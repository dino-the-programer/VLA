FROM python:3.8-alpine

ARG workDir="app"
WORKDIR /${workDir}

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000 5000

#CMD ["python3", "-m", "uvicorn", "main:app", "--host=0.0.0.0"]