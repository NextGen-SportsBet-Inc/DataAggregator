# DataAggregator
Microservice responsible for the data collection.

# How to run

1. Get `.env` to ./DataAggregator

2. Run:

    ```bash
    docker compose up --build
    ```

# Usefull comands:

- Clean pycache

    ```bash
    find . -type d -name "__pycache__" -print0 | xargs -0 rm -r
    ```

- Commit and push

    ```bash
    git add .
    git commit -m 'commit name'
    git push origin YOUR_BRANCH_NAME
    ```
