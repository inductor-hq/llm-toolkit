# Text to SQL LLM App

## Inductor Open-Source LLM App Starter Templates
This app is part of the Inductor open-source LLM app starter templates, which are designed to help developers quickly build and deploy LLM apps using Inductor. For more information and additional templates, visit the [Inductor LLM Toolkit GitHub repository](https://github.com/inductor-hq/llm-toolkit) and [Inductor blog](https://inductor.ai/blog).

## App Overview
This app transforms a data-related question into a SQL query for the specified database, executes the query, and returns the results if the query is valid. It is designed to be simple, easy to use, and easy to customize. To ensure accessibility to developers using various LLM frameworks or none at all, it does not rely on any specific frameworks (such as LlamaIndex or LangChain). However, you can easily adapt the code to incorporate your preferred framework.

### Technical Details

There are two main components to this app: the database functions (`database.py`) and the app itself (`app.py`).

1. **Database Functions** (`database.py`):
   - **Schema Generation**: This function retrieves the database table schema for the specified SQL database. 
   - **Validity Testing**: Given a SQL query, test to see if it is a valid query.
   - **SQL Execution**: Run a SQL query on the specified database and return the results.

2. **SQL Generation and Processing** (`app.py`):
   - **SQL Generation**: The app uses an LLM  (OpenAI `gpt-4o`) to generate a SQL query that answers a given request in the context of the retrieved database schema.
   - **SQL Processing**: Processes the generated SQL to address common issues with LLM generated SQL (e.g. missing `;` or prepending `sql`) and executes it if valid. Both the original and processed SQL are returned for validation and debugging purposes.

### Files
- `database.py`: Specifies the connection to the SQL database as well as the database type. Provides functions for schema retrieval and SQL query execution. 

- `app.py`: Entrypoint for the Text to SQL LLM app.

- `prompts.py`: Contains the base prompt used for querying the LLM model.

- `test_suite.py`: An Inductor test suite for the Text to SQL app. It includes a set of test cases, quality measures, and hyperparameters to systematically test and evaluate the app's performance.

- `quality_measures.py`: Contains Python functions that implement Inductor quality measures, which are imported and used in `test_suite.py`.

- `requirements.txt`: Specifies the required Python package dependencies for the app.

- `sample.db`: A sample (synthetically generated) ecommerce SQLite database that this app is configured to work with by default. See [How to Modify This Template to Run on Your Own SQL Database](#how-to-modify-this-template-to-run-on-your-own-sql-database) for instructions on how to customize the app to use your SQL database.

## Useful Commands
- `inductor playground app:generate_sql`: Start an Inductor playground to generate SQL queries from text inputs.

- `inductor playground app:get_analytics_results`: Start an Inductor playground to generate SQL queries from text inputs and return the results from executing those queries.

- `python test_suite.py`: Run the test suite to evaluate the performance of the Text to SQL app.

## How to Configure and Run This App

1. **Clone this GitHub repository:**
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Create an environment variable containing your OpenAI API key:**
   ```sh
   export OPENAI_API_KEY=<your_openai_api_key>
   ```

4. **Run the LLM app:**
   - Start your Python interpreter:
     ```sh
     python
     ```
   - Import the main entrypoint function for this app:
     ```python
     from app import get_analytics_results
     ```
   - Run the app function with a question as input:
     ```python
     print(get_analytics_results("Show me the three most expensive orders with all order data"))
     ```

See [How to Modify This Template to Run on Your Own SQL Database](#how-to-modify-this-template-to-run-on-your-own-sql-database) for instructions on how to customize the app to use your SQL database.

## How to Use Inductor to Iterate on, Test, Improve, and Monitor This App

Note: when you run any of the Inductor commands in this section, you will be prompted to log in to Inductor or create an account (for free) if you don't already have one.  Alternatively, if you don't already have an account, you can sign up [here](https://inductor.ai/).

1. **Auto-generate a playground UI:**
   - Run the following command to instantly auto-generate a playground UI that makes it easy to interactively experiment with, and share, your Text to SQL LLM app:
     ```sh
     inductor playground app:get_analytics_results
     ```

2. **Modify and run the included test suite to evaluate your LLM app:**
   - If you haven't modified the app to point at your own SQL database, then the included test suite can be run as is. If you _have_ modified the app to point at your own SQL database, then open `test_suite.py` and modify the test cases therein to reflect your particular use case.
   - Run the test suite, which will also generate a link to view the test results in your browser:
     ```sh
     python test_suite.py
     ```

3. **Use hyperparameters to systematically improve your LLM app:**
   - Open `test_suite.py` and add another value to the hyperparameter specification (`inductor.HparamSpec`) named "model".
   - Re-run the test suite to assess the performance of this new variant of the LLM app and compare it to the variants that you've already been testing:
     ```sh
     python test_suite.py
     ```

4. **Utilize live logging and monitoring of your LLM app's execution:**
   - Emulate running your LLM app live by starting your Python interpreter and directly executing the LLM app's main entrypoint function:
     ```python
     from app import get_analytics_results
     get_analytics_results("Show me the three most expensive orders with all order data")
     ```
   - Because the `get_analytics_results` function is decorated with the `@inductor.logger` decorator (see `app.py`), Inductor automatically logs its inputs, outputs, and other details of its execution (e.g., the unprocessed SQL returned from the LLM). To view these logs, visit your Inductor dashboard and navigate to "LLM programs" -> "app:get_analytics_results" -> "View live executions".

## How to Modify This Template to Run on Your Own SQL Database

This app is initially set up to work on a sample (synthetically generated) ecommerce SQLite database. The sample database was set up with a sample schema and generated synthetic data. You can quickly and easily run this app on your own database instead, by following the below steps.

1. **Database:**
   - Open `database.py` and update the `sql_database_type` variable to the type of your SQL database (PostrgreSQL, MySQL, SQLite, etc.) and update the `_engine` variable to create a SQLAlchemy engine connection to your database. See [SQLAlchemy Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls) for more information. Connecting to different database types may require additional dependencies (e.g. psycopg2 for PostgreSQL). We recommend giving the LLM app access to your database only via a database role that provides only read-only database access.

2. **Test Cases:**
   - Open `test_suite.py` and modify the test cases specified therein (and/or add additional test cases) to reflect your use case.
