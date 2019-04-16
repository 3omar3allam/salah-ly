## Startup

1. Create virtual environment: (first time only)

    navigate to project folder, then:

    * Linux:
    ```
    python3 -m venv venv
    ```
    * Windows:
    py -3 -m venv venv

2. Activate environment: (every time)

    from your working terminal:

    * Linux:
    ```
    . venv/bin/activate
    ```

    * Windows:
    ```
    venv\Scripts\activate
    ```

3. Instal dependencies: (every pull)

    ```
    pip install -r requirements.txt
    ```

## Running development server

```
flask run
```

## Note
Before every commit run: `pip freeze > requirements.txt` to save your new packages