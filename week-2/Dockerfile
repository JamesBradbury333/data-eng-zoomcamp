FROM prefecthq/prefect:2.7.7-python3.10

COPY docker-requirements.txt . 

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY gcp/parameterized_flow.py /opt/prefect/flows
RUN mkdir -p /opt/prefect/data/yellow