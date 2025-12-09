FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8050
ENV HOST=0.0.0.0
EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "src.app:server"]