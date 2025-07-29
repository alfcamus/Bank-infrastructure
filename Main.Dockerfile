FROM python:3.13-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "-m", "controller.MainBankController"]