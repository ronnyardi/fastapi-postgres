# Pull base image menggunakan Python:3.8.10-alpine3.13
FROM python:3.8.10-alpine3.13

# Set the working directory
WORKDIR /app

# Menyalin requirement.txt ke dalam Workdir
COPY requirement.txt requirement.txt

# Melakukan instalasi dependensi untuk psycopg2 dan requirement service
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip3 install --no-cache-dir -r requirement.txt && \
 apk --purge del .build-deps

# Menyalin source code ke dalam Workdir
COPY ./app .

# Perintah untuk menjalankan uvicorn di localhost dan port 5555
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555", "--reload"]

# Set port untuk mengekspos service ke port 5555
EXPOSE 5555