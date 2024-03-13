FROM python:3.10

WORKDIR .

# Copy the project files to the working directory
COPY . /app/backend

RUN cd /app/backend && pip install -r requirements.txt

# Expose the port that Django runs on (default is 8000)
EXPOSE 8000