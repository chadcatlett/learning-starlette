FROM python:3.10-slim

# expose port 8000
EXPOSE 8000/tcp

RUN python -m pip install -U PDM && \
    mkdir /app

WORKDIR /app
COPY . /app

# ensure dependencies are installed
RUN pdm sync

# run main.py This is not ideal, but works.
CMD ["pdm", "run", "python", "main.py"]
