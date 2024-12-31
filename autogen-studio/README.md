
# https://pypi.org/project/autogenstudio/

## Run Locally
# https://microsoft.github.io/autogen/0.2/docs/autogen-studio/getting-started#running-the-application
git clone https://github.com/microsoft/autogen.git
export OPENAI_API_KEY=""

autogenstudio ui --help
autogenstudio ui --host 0.0.0.0 --port 8088 --appdir ./work_dir --database-uri postgresql+psycopg://user:password@192.168.50.50/autogen     # pragma: allowlist secret


## Run in Docker
docker run -d -it -p 8088:8088 --name autogenstudio -v $(pwd):/app:ro bitnami/python:3.12.7 bash docker_run.sh

# Open Terminal in Docker Running Container
docker attach autogenstudio

docker run -d -it -p 8088:8088 --name autogenstudio -v $(pwd):/app:ro bitnami/python:3.12.7 pip install -r requirements.txt && "autogenstudio ui --host 0.0.0.0 --port 8088 --database-uri postgresql+psycopg://adminuser:12345@192.168.50.50/autogen"


export AUTOGENSTUDIO_DATABASE_URI=postgresql+psycopg://adminuser:12345@192.168.50.50/autogen
export AUTOGENSTUDIO_UPGRADE_DATABASE=1
export AUTOGENSTUDIO_APPDIR=./work_dir

autogenstudio ui --host 0.0.0.0 --port 8088

## Testing
docker run -d -it -p 8088:8088 -v $(pwd):/app:ro bitnami/python:3.12.7 bash sleep 30m
