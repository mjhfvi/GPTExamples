docker run -it --name autogenstudio-temp -v $(pwd):/app:ro bitnami/python:3.11.10 pip install -r requirements.txt

docker commit autogenstudio-temp autogenstudio-new

docker run -it -p 8081:8081 -e OPENAI_API_KEY="" autogenstudio-new autogenstudio ui --host 0.0.0.0 --port 8081 --database-uri postgresql+psycopg://adminuser:12345@192.168.50.50/autogen
