FROM python:3.9
RUN pip3 install fastapi
RUN pip3 install uvicorn
RUN pip3 install requests
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]