FROM python:3
EXPOSE 8000
ARG UID=1000
ARG GID=1000

WORKDIR /app

# Python venv and requirements
RUN pip install --upgrade pip
RUN pip install virtualenv && virtualenv -p python /app/venv
COPY requirements.txt ./
RUN /app/venv/bin/pip install -r requirements.txt

# get app code
RUN mkdir /app/shiftplan
COPY ./TheShiftplan/ /app/shiftplan

# latest migrations
RUN /app/venv/bin/python /app/shiftplan/manage.py makemigrations

RUN groupadd -g "${GID}" shift_user \
  && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" shift_user
RUN chown -R shift_user:shift_user /app/shiftplan
USER shift_user

WORKDIR /app/shiftplan

ENV PYTHONUNBUFFERED = 1
CMD ["/app/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
