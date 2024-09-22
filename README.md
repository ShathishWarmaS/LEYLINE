# FastAPI Application

This project provides a REST API built with FastAPI, including several endpoints and integrated with a PostgreSQL database. The API is ready for production, with Docker and Kubernetes (Helm) support.

## Features

- **/metrics**: Prometheus metrics
- **/health**: Health check endpoint
- **/v1/tools/lookup**: Lookup IPv4 addresses for a given domain and log the queries
- **/v1/tools/validate**: Validate if the input is an IPv4 address
- **/v1/history**: Retrieve the latest 20 saved queries

## Requirements

- Python 3.11
- Docker
- PostgreSQL
- Kubernetes
- Helm

## Setup and Run

### Local Development

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/fastapi-app.git
    cd fastapi-app
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port ${SERVICE_PORT}
     uvicorn app.main:app --reload --host 0.0.0.0 --port 3000```

### Docker

1. **Build and run the Docker containers**:
    ```sh
    docker-compose up -d --build
    ```

2. **Access the application**:
    - API: `http://localhost:3000`
    - Swagger UI: `http://localhost:3000/docs`
    - Swagger : `http://localhost:3000/redocs`
### Kubernetes Deployment

1. **Package the Helm chart**:
    ```sh
    helm package helm/fastapi-app
    ```

2. **Install the Helm chart**:
    ```sh
    helm install fastapi-app ./fastapi-app-0.1.0.tgz
    ```

3. **Monitor the deployment**:
    ```sh
    kubectl get pods
    ```

### CI/CD Pipeline

- The CI/CD pipeline is configured using GitHub Actions and is triggered on every push or pull request to the `main` branch. The pipeline includes steps for linting, testing, Docker image builds, and Helm packaging.

### Deployment to Kubernetes

1. **Deploy the application to a Kubernetes cluster**:
    ```sh
    helm install fastapi-app helm/fastapi-app
    ```

2. **Verify the deployment**:
    ```sh
    kubectl get all
    ```

### Environment Variables

Ensure the following environment variables are set:

- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql://user:password@db:5432/domain_lookup`)
- `DOMAIN`: The domain name used by the application.
- `API_VERSION`: Version of the API.
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins.
- `SERVICE_PORT`: Port on which the service runs.
- `LOG_LEVEL`: Logging level for the application.

## References

- [12 Factor App](https://12factor.net/)
- [Swagger](https://swagger.io/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)
- [Helm](https://helm.sh/)
