# app/Dockerfile

FROM python:3.11.4-bullseye

WORKDIR /app
COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt



COPY . /app
EXPOSE 8501

CMD streamlit run /app/app.py