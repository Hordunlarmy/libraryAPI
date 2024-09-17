# Use the base image
FROM base AS frontend

WORKDIR /workspace/library/frontend_api

COPY src/frontend_api/ .

EXPOSE 8001

# CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "main:app"]
CMD ["poetry", "run", "python3", "main.py"]
