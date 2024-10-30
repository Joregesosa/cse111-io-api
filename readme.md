# IO API

## Description

This project is a financial management API built with FastAPI. It provides endpoints for managing categories, authentication, incomes, expenses, and balance calculations. The API includes middleware for authentication and various routers to handle different aspects of financial data.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Joregesosa/cse111-io-api.git
    cd cse111-io-api
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On Unix or MacOS
    source .venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Project

To run the FastAPI project, use the following command:
```sh
fastapi dev app/main.py
```

## Running tests

To run the FastAPI project, use the following command:
```sh
pytest
```