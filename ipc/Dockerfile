FROM gcc:latest

WORKDIR /app
COPY . .

RUN apt update && apt install -y python3-pip
RUN pip3 install fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
