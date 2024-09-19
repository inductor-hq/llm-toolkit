# Chat with PDF Bot (RAG-based LLM App)

## Inductor Open-Source LLM App Starter Templates
This app is part of the Inductor open-source LLM app starter templates, which are designed to help developers quickly build and deploy LLM apps using Inductor. For more information and additional templates, visit the [Inductor LLM Toolkit GitHub repository](https://github.com/inductor-hq/llm-toolkit) and [Inductor blog](https://inductor.ai/blog).

## App Overview
This app implements a chatbot that answers questions about PDF documents. It is designed to be simple, easy to use, and easy to customize. To ensure accessibility to developers using various LLM frameworks or none at all, it does not rely on any specific frameworks (such as LlamaIndex or LangChain). However, you can easily adapt the code to incorporate your preferred framework.

### Technical Details

There are two main components to this app: the setup script (`setup_db.py`) and the app itself (`app.py`).

1. **Vector Database Setup** (`setup_db.py`):
   - **Chunking**: The script processes one or more PDF files using [Unstructured](https://docs.unstructured.io/welcome), chunking them by title.
   - **Embedding**: Each section is converted into an embedding using Sentence-Transformers' `all-MiniLM-L6-v2` model (the default model for ChromaDB).
   - **Vector Database**: The embeddings, along with their associated chunks and metadata, are stored locally at `./chroma` using ChromaDB.

2. **Retrieval and Answer Generation** (`app.py`):
   - **Retrieval**: The app queries the vector database to retrieve the most relevant chunks based on the chat session's embedding, which is generated using the same Sentence-Transformers model as in the setup script.
   - **Answer Generation**: The chat session and retrieved chunks are passed to the OpenAI `gpt-4o` model, which generates an answer to the question.

### Files
- `setup_db.py`: Processes the PDF files using [Unstructured](https://docs.unstructured.io/welcome) and loads the relevant information into a vector database (ChromaDB). This includes parsing the files, chunking the text into meaningful sections, and storing embeddings of each section along with relevant metadata into a vector database.

- `app.py`: Entrypoint for the Chat with PDF bot app.

- `prompts.py`: Contains the prompts used to query the LLM.

- `test_suite_[*]`: Inductor test suites for the Chat with PDF bot. Each test suite includes a set of test cases, quality measures, and hyperparameters to systematically test and evaluate the app's performance.

- `quality_measures.py`: Defines the Inductor quality measure functions that are used for evaluating test case executions within test suites. 

- `test/`: Directory containing all the relevant files for running Inductor test suites.
    - `pdf[*]_test_cases.py`: Contain Inductor test cases specific to individual pdfs.
    - `pdf_combined_test_cases.py`: Contains test cases with questions that reference multiple pdfs.

- `requirements.txt`: Specifies the required Python package dependencies for the app.

## Useful Commands
- `python setup_db.py`: Create and populate the vector database (locally stored at `./chroma`). If the database already exists, this script will reset and repopulate it. Running this script is required before running the app or any test suite.

- `inductor playground app:chat_with_pdf`: Start an Inductor playground to interact with the Chat with PDF bot.

- `python test_suite_all.py`: Run the full test suite (all test cases for all pdfs) to evaluate the performance of the Chat with PDF bot.

## How to Configure and Run This App

1. **Clone this GitHub repository:**
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Install other dependencies:**

To use [Unstructured](https://github.com/Unstructured-IO/unstructured?tab=readme-ov-file#installing-the-library) for PDF parsing, it is recommended to have the following system dependencies installed: 
   - tesseract: For more information and installation methods, see [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)
   - poppler: For installation methods, see [here](https://pdf2image.readthedocs.io/en/latest/installation.html)

   **MacOS**
   ```sh
   brew install tesseract
   brew install poppler
   ```
   **Ubuntu**
   ```sh
   sudo apt update && sudo apt-get -y install tesseract-ocr
   sudo apt update && sudo apt-get -y install poppler-utils
   ```

4. **Create an environment variable containing your OpenAI API key:**
   ```sh
   export OPENAI_API_KEY=<your_openai_api_key>
   ```

5. **Populate the vector database:**
   ```sh
   python setup_db.py
   ```

6. **Run the LLM app:**
   - Start your Python interpreter:
     ```sh
     python
     ```
   - Import the main entrypoint function for this app and the inductor library:
     ```python
     from app import chat_with_pdf
     import inductor
     ```
   - Run the app function with a question as input:
     ```python
     print(chat_with_pdf(inductor.ChatSession(messages=[{"content":"How many parameters is GPT-3 trained on?", "role":"user"}])))
     ```

See [How to Modify This Template to Run on Your Own PDF Documents](#how-to-modify-this-template-to-run-on-your-own-pdf-documents) for instructions on how to customize the app to use your own PDF document(s).

## How to Use Inductor to Iterate on, Test, Improve, and Monitor This App

Note: when you run any of the Inductor commands in this section, you will be prompted to log in to Inductor or create an account (for free) if you don't already have one.  Alternatively, if you don't already have an account, you can sign up [here](https://inductor.ai/).

1. **Auto-generate a playground UI:**
   - Run the following command to instantly auto-generate a playground UI that makes it easy to interactively experiment with, and share, your Chat with PDF LLM app:
   ```sh
   inductor playground app:chat_with_pdf
   ```

2. **Modify and run the included test suite(s) to evaluate your LLM app:**
   - An example of the results of running `test_suite_all.py` can be found [here](https://app.inductor.ai/test-suite/run/2616). Running this test suite will call OpenAI (or the LLM provider of your choice) a number of times, so it is good to be mindful of the cost. Running this test suite with OpenAI gpt-4o costs less than $0.50 at the time of this publishing.
   - If you haven't modified the app to point at your own PDF documents, then the included test suite(s) can be run as is. If you _have_ modified the app to point at your own PDF documents, then open `test/pdf[*]_test_cases.py` and modify the test cases therein to reflect your particular use case.
   - Run the test suite, which will also generate a link to view the test results in your browser:
     ```sh
     python test_suite_pdf[*].py
     ```
     or
     ```sh
     python test_suite_all.py
     ```

3. **Use hyperparameters to systematically improve your LLM app:**
   - Inductor tests all combinations of values of the hyperparameters included in a test suite, so the number of LLM app executions performed in running a test suite can increase rapidly as you increase the number of included hyperparameters. Although this can significantly reduce development time, it can also result in incurring non-trivial cost from your LLM provider if larger numbers of hyperparameters are used simultaneously. It is important to be mindful of what and how many hyperparameters are being used for each test suite run. For example, running test_suite_all.py after uncommenting all hyperparameters defined in that file would result in 16 (2*2*2*2) calls for each of the 26 test cases, in turn resulting in 416 (16*26) test case executions, which can result in non-trivial cost from LLM providers (depending on the provider and model used).
   - Open `test_suite_pdf[*].py` and add another value to the hyperparameter specification (`inductor.HparamSpec`) named "query_result_num".
   - Re-run the test suite to assess the performance of this new variant of the LLM app and compare it to the variants that you've already been testing:
     ```sh
     python test_suite_pdf[*].py
     ```

4. **Utilize live logging and monitoring of your LLM app's execution:**
   - Emulate running your LLM app live by starting your Python interpreter and directly executing the LLM app's main entrypoint function:
     ```python
     from app import chat_with_pdf
     import inductor
     chat_with_pdf(inductor.ChatSession(messages=[{"content":"How many parameters is GPT-3 trained on?", "role":"user"}]))
     ```
   - Because the `chat_with_pdf` function is decorated with the `@inductor.logger` decorator (see `app.py`), Inductor automatically logs its inputs, outputs, and other details of its execution (e.g., the text snippets retrieved by the underlying RAG system). To view these logs, visit your Inductor dashboard and navigate to "LLM programs" -> "app:chat_with_pdf" -> "View live executions".

## How to Modify This Template to Run on Your Own PDF Documents

This app is initially set up to work by default on the following publicly available PDFs:
- [Attention Is All You Need](https://arxiv.org/pdf/1706.03762)
- [Language Models are Few-Shot Learners](https://arxiv.org/pdf/2005.14165)
- [GPT-4 Technical Report](https://arxiv.org/pdf/2303.08774)

You can quickly and easily run this app on any other set of PDFs by following the following instructions.

1. **Documents:**
   - Open `setup_db.py` and update the `PDF_FILES` variable to point to your PDF document(s). These can be file_paths or urls that link to PDFs.

2. **Prompts:**
   - Open `prompts.py` and update the prompts therein to better suit your use case. (This may not be necessary, as the default prompt is reasonably general).

3. **Test Cases:**
   - Open `test/pdf[*]_test_cases.py` and modify the test cases specified therein (and/or add additional test cases) to reflect your use case.
    - Alternatively, create new test cases files for your specific PDFs.

## Additional Notes

### On PDF Parsing
Parsing is one of the most fundamental components of RAG-based LLM apps, so it is important to thoroughly explore the most effective parsing tools and techniques for your specific use case. In creating this template, we only considered (and used) free and open source PDF parsers (e.g., licensed under Apache or MIT licenses) in order to ensure ease of use of the template. Within these constraints, we have found Unstructured to perform well on the default PDFs in this template.

In `setup_db.py`, we utilize Unstructured's `partition_pdf` function for PDF parsing. While we only use its basic functionality here, that function offers additional options that can potentially enhance performance. For instance, setting parameters such as `infer_table_structure=True` and `strategy="hi_res"` may improve how tables and images are handled, though this may increase compute time and resource usage. For further details, refer to [Unstructured's documentation](https://docs.unstructured.io/open-source/core-functionality/partitioning#partition-pdf).

There are also paid PDF parsing options, as well as open source options with more restrictive licenses (e.g., GNU AGPL), such as [PyMuPDF](https://github.com/pymupdf/PyMuPDF).  Depending on your needs, it may be beneficial to consider such options, which you can swap in to be used in place of Unstructured within this LLM app.

### On External Libraries
Although the libraries on which this app relies directly are version-locked within the app's configuration, some of these libraries do not version-lock their own dependencies. As a result, it is possible that incompatibilities between the versions of indirect dependencies could temporarily arise. If you experience such an incompatibility, please file a GitHub issue on this repository, and we will aim to resolve it rapidly.