"""Documentation Question-Answering (Q&A) Bot"""
import os

import inductor
import openai

import prompts
import setup_db


openai_client = openai.OpenAI()


# Explicitly set the tokenizers parallelism to false to avoid transformers
# warnings.
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def rephrase_question(question: str) -> str:
    """Rephrase the user's question in a specific context.

    Uses an LLM to rephrase the user's question in the context of a
    specific subject matter, as defined by the rephrase prompt. The rephrased
    question is intended to provide a more informative and relevant vector DB
    query by incorporating more relevant keywords and phrases.

    Args:
        question: The user's question.

    Returns:
        The question rephrased in a specific context.
    """
    rephrase_prompt_system = inductor.hparam(
        "rephrase_prompt",
        prompts.REPHRASE_PROMPT_DEFAULT)
    rephrase_prompt_user = (
        "Rephrase the following question to fit the context of the "
        "provided subject matter.\n"
        f"QUESTION:\n{question}")

    response = openai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": rephrase_prompt_system},
            {"role": "user", "content": rephrase_prompt_user}],
        model="gpt-4o")
    rephrase_response = response.choices[0].message.content
    return rephrase_response


@inductor.logger
def documentation_qa(question: str) -> str:
    """Answer a question about one or more markdown documents.

    Args:
        question: The user's question.
    
    Returns:
        The answer to the user's question.
    """
    try:
        collection = setup_db.chroma_client.get_collection(
            name=setup_db.COLLECTION_NAME)
    except ValueError as error:
        print("Vector DB collection not found. Please create the collection "
              "by running `python3 setup_db.py`.")
        raise error

    # Decide whether to use the user's original question or a version of the
    # question rephrased by an LLM as the query text for the vector DB.
    # The rephrased question is intended to provide a more informative and
    # relevant vector DB query by incorporating more relevant keywords and
    # phrases. However, this RAG strategy is not universally effective and
    # incurs additional latency and cost due to the additional LLM API call
    # used to generate the rephrased question. We use a hyperparameter to
    # toggle this strategy on or off, enabling easy experimentation and
    # evaluation of the strategy's effectiveness.
    vector_query_text_type = inductor.hparam(
        "vector_query_text_type", "rephrase")
    if vector_query_text_type == "rephrase":
        rephrased_question = rephrase_question(question)
        query_text = rephrased_question
    else:
        query_text = question
    inductor.log(query_text, name="vector_query_text")

    query_result = collection.query(
        query_texts=[query_text],
        n_results=inductor.hparam("vector_query_result_num", 4))
    documents = query_result["documents"][0]
    metadatas = query_result["metadatas"][0]
    inductor.log(query_result, name="vector_query_result")

    contexts = []
    for document, metadata in zip(documents, metadatas):
        context = (
            "CONTEXT: " + document + "\n\n"
            "REFERENCE: " + metadata.get("url", "N/A") + "\n\n")
        contexts.append(context)
    contexts = "\n\n".join(contexts)
    inductor.log(contexts, name="contexts")

    prompt = inductor.hparam("main_prompt", prompts.MAIN_PROMPT_DEFAULT)
    prompt += f"CONTEXTs:\n{contexts}"

    response = openai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}],
        model="gpt-4o")
    response = response.choices[0].message.content
    return response
