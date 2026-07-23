FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .[api,dashboard,excel]
EXPOSE 8000 8501
CMD ["python","-m","brinevalue.cli","demo","--index","0"]
