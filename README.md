## Pastebin DRF

## First start
@TODO

## Run
1. Run containers
```shell
make up
```

2. In new terminal, run worker
    ```shell
    make run-worker
    ```

3. In new terminal, run celery beat
    ```shell
    make run-celery-beat
    ```

4. Go to http://127.0.0.1:8000/api/swagger-ui