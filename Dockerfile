# For more information, please refer to https://aka.ms/vscode-docker-python.
FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container.
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging.
ENV PYTHONUNBUFFERED=1

# Set working directory.
WORKDIR /code

# Creates a non-root user with an explicit UID and adds permission to access the /code folder.
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers.
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

# Install pip requirements.
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug.
CMD ["python", "./code/main.py"]