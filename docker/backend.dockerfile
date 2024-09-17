# Use the base image
FROM base AS backend

WORKDIR /workspace/library/backend_api

COPY src/backend_api/ .

EXPOSE 8002

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]

