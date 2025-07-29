FROM python:3.13-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 3001
ENTRYPOINT ["python", "-m", "webapp.FrontEndController"]