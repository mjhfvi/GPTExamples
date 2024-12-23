docker run -it --name autogenstudio-temp -v $(pwd):/app:ro bitnami/python:3.11.10 pip install -r requirements.txt

docker commit autogenstudio-temp autogenstudio-new

docker run -it -p 8081:8081 -e OPENAI_API_KEY="" autogenstudio-new autogenstudio ui --host 0.0.0.0 --port 8081 --database-uri postgresql+psycopg://user:pass@192.168.50.50/autogen  # pragma: allowlist secret

## chromadb Manage Tools
docker run -p 3002:3002 -e SERVER_PORT="3002" -e JWT_SECRET="" -e SYS_EMAIL="mjhfvi@gmail.com" -e SYS_PASSWORD="" -e DATABASE_CONNECTION_STRING="postgresql://user:pass@172.22.54.208:5432/vectoradmin" mintplexlabs/vectoradmin    # pragma: allowlist secret

docker run -p 3000:3000 fengzhichao/chromadb-admin

docker run -p 3001:3001 -e SERVER_PORT="3001" -e JWT_SECRET="" -e INNGEST_EVENT_KEY="background_workers" -e INNGEST_SIGNING_KEY="" -e INNGEST_LANDING_PAGE="true" -e DATABASE_CONNECTION_STRING="postgresql://user:pass@172.22.54.208:5432/vectoradmin" mintplexlabs/vectoradmin    # pragma: allowlist secret
