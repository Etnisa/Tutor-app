FROM python

WORKDIR /TutorFrontend

COPY app.py .
COPY constants.py .
COPY helpers.py .
COPY routes.py .
COPY requirements.txt .
COPY static /TutorFrontend/static
COPY templates /TutorFrontend/templates

RUN pip install -r requirements.txt

RUN pip install gunicorn

# CMD ["python", "run.py"]

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8081", "app:app"]
