# Documentation Question-Answering (Q&A) Bot (RAG-based LLM App)

## Inductor Open-Source LLM App Starter Templates
This app is part of the Inductor open-source LLM app starter templates. These templates are designed to help developers quickly build and deploy LLM apps using Inductor. For more information and additional templates, visit the [Inductor LLM Toolkit GitHub repository](https://github.com/inductor-hq/llm-toolkit) and [Inductor blog](https://inductor.ai/blog/open-sourcing-llm-app-starter-templates).

## App Overview
This app answers questions about Markdown documents. It is designed to be simple, easy to use, and easy to customize. To ensure accessibility to developers using various LLM frameworks or none at all, it does not rely on any specific frameworks (such as LlamaIndex or LangChain). However, you can easily adapt the code to incorporate your preferred framework.

### Technical Details

There are two main components to this app: the setup script (`setup_db.py`) and the app itself (`app.py`).

1. **Vector Database Setup** (`setup_db.py`):
   - **Chunking**: The script processes one or more Markdown files, splitting them by Markdown sections.
   - **Embedding**: Each section is converted into an embedding using Sentence-Transformers' `all-MiniLM-L6-v2` model (the default model for ChromaDB).
   - **Vector Database**: The embeddings, along with their associated chunks and metadata, are stored locally at `./chroma` using ChromaDB.

2. **Retrieval and Answer Generation** (`app.py`):
   - **Retrieval**: The app queries the vector database to retrieve the most relevant chunks based on the question's embedding, which is generated using the same Sentence-Transformers model as in the setup script.
   - **Answer Generation**: The question and retrieved chunks are passed to the OpenAI `gpt-4o` model, which generates an answer to the question.

### Files
- `sample.md`: The default Markdown document that the app uses to answer questions. See [How to Modify This Template to Run on Your Own Markdown Documents](#how-to-modify-this-template-to-run-on-your-own-markdown-documents) for instructions on how to customize the app to use your Markdown document(s). This Markdown file is from the [Pydantic 2.8 documentation](https://docs.pydantic.dev/2.8/concepts/models/) and is accessible on [GitHub](https://github.com/pydantic/pydantic/blob/main/docs/concepts/models.md) under the MIT license.

- `setup_db.py`: Processes the Markdown files and loads the relevant information into a vector database (ChromaDB). This includes parsing the files, chunking the text into meaningful sections, and storing embeddings of each section along with relevant metadata into a vector database.

- `app.py`: Entrypoint for the documentation Q&A bot app.

- `test_suite.py`: An Inductor test suite for the documentation Q&A bot. It includes a set of test cases, quality measures, and hyperparameters to systematically test and evaluate the app's performance.

- `test_cases.yaml`: Contains the test cases used in the test suite (referenced by `test_suite.py`). We separate the test cases into their own file to keep `test_suite.py` clean and readable; one could alternatively include the test cases directly in `test_suite.py`.

- `requirements.txt`: Specifies the required Python package dependencies for the app.

## Useful Commands
- `python setup_db.py`: Create and populate the vector database (locally stored at `./chroma`). If the database already exists, this script will reset and repopulate it. Running this script is required before running the app or test suite.

- `inductor playground app:documentation_qa`: Start an Inductor playground to interact with the documentation Q&A bot.

- `python test_suite.py`: Run the test suite to evaluate the performance of the documentation Q&A bot.

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

4. **Populate the vector database:**
   ```sh
   python setup_db.py
   ```

5. **Run the LLM app:**
   - Start your Python interpreter:
     ```sh
     python
     ```
   - Import the main entrypoint function for this app:
     ```python
     from app import documentation_qa
     ```
   - Run the app function with a question as input:
     ```python
     print(documentation_qa("What is Pydantic?"))
     ```

See [How to Modify This Template to Run on Your Own Markdown Documents](#how-to-modify-this-template-to-run-on-your-own-markdown-documents) for instructions on how to customize the app to use your Markdown document(s).

## How to Use Inductor to Iterate on, Test, Improve, and Monitor This App

Note: when you run any of the Inductor commands in this section, you will be prompted to log in to Inductor or create an account (for free) if you don't already have one.  Alternatively, if you don't already have an account, you can sign up [here](https://app.inductor.ai/signup).

1. **Auto-generate a playground UI:**
   ```sh
   inductor playground app:documentation_qa
   ```

2. **Modify and run the included test suite:**
   - If you haven't modified the app to point at your own Markdown documents, then the included test suite can be run as is. If you _have_ modified the app to point at your own Markdown documents, then open `test_cases.yaml` and modify the test cases therein to reflect your particular use case.
   - Run the test suite, which will also generate a link to view the test results in your browser:
     ```sh
     python test_suite.py
     ```

3. **Use hyperparameters to systematically improve your LLM app:**
   - Open `test_suite.py` and add another value to the hyperparameter specification (`inductor.HparamSpec`) named "vector_query_result_num".
   - Re-run the test suite to assess the performance of this new variant of the LLM app and compare it to the variants that you've already been testing:
     ```sh
     python test_suite.py
     ```

4. **Utilize live logging and monitoring of your LLM app's execution:**
   - Emulate running your LLM app live by starting your Python interpreter and directly executing the LLM app's main entrypoint function:
     ```python
     from app import documentation_qa
     documentation_qa("What is Pydantic?")
     ```
   - Because that function is decorated with the `@inductor.logger` decorator (see `app.py`), Inductor automatically logs its inputs, outputs, and other details of its execution (e.g., the text snippets retrieved by the underlying RAG system). To view these logs, visit your Inductor dashboard and navigate to "LLM programs" -> "app:documentation_qa" -> "View live executions".

## How to Modify This Template to Run on Your Own Markdown Documents

1. **Documents:**
   - Open `setup_db.py` and update the `MARKDOWN_FILES` variable to point to your Markdown document(s).

2. **Prompts:**
   - Open `prompts.py` and update the prompts therein to better suit your use case. The prompts are also set up as hyperparameters to allow you to experiment with prompts in the Inductor playground and test suite. To enable systematic prompt experimentation as you run the test suite, uncomment and modify the hyperparameter variables `main_prompt` and `rephrase_prompt` (i.e., the `inductor.HparamSpec` instances) in `test_suite.py`.

3. **Test Cases:**
   - Open `test_cases.yaml` and modify the test cases specified therein (and/or add additional test cases) to reflect your use case.
