## Pastebin DRF

## Requirements
- Python >= 3.12
- Docker >= 24.0.5

## First start
Run commands
```shell
make up
make db-migrate
```

## Run
1. Run containers
   ```shell
   make up
   ```

2. In new terminal, run http-server
    ```shell
    make run-http-server
    ```

4. Go to http://127.0.0.1:8000/api/swagger-ui