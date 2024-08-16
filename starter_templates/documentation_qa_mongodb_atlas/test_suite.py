"""Test Suite for Documentation Question-Answering (Q&A) Bot"""
import os
import textwrap
from typing import Any, Dict

import inductor
import openai

import prompts


llm_client = openai.OpenAI()


test_suite = inductor.TestSuite(
    id_or_name="documentation_qa",
    llm_program="app:documentation_qa")


# Add test cases from a separate YAML file. Inductor test suite components
# (e.g. test cases, quality measures, hyperparameters, etc.) can be defined
# interchangeably in YAML or Python formats. In this case, the test cases
# are defined in a YAML file for readability of long texts.
current_directory = os.path.dirname(os.path.abspath(__file__))
test_suite.add(os.path.join(current_directory, "test_cases.yaml"))


def can_question_be_answered_with_context(
    _,
    test_case_inputs: Dict[str, Any],
    test_case: inductor.TestCase,
    execution_details: inductor.ExecutionDetails) -> str:
    """Evaluate if the question can be answered with the provided context.

    Intended to be used as a quality measure.

    Args:
        test_case_inputs: Inputs for the test case that was used in the LLM
            app execution.
        test_case: Test case that was used in the LLM app execution.
        execution_details: Details of the LLM app execution, including logged
            values.
    
    Returns:
        An LLM response indicating if the question can be answered with the
        provided context.
    """
    # In the target answer, "INVALID", is shorthand used to indicate that the
    # question should not be answered. In this case this quality measure should
    # always return True, as "INVALID" should be returned by the LLM program
    # regardless of the context.
    target_answer = test_case.output
    if target_answer == "INVALID":
        return True

    # The context sent to the LLM is logged under the name "contexts".
    # It can be retrieved from the execution details.
    contexts = execution_details.logged_values_dict.get("contexts")
    # If for some reason the context was not logged, short-circuit the
    # evaluation and return False.
    if contexts is None:
        return False

    question = test_case_inputs["question"]
    prompt = textwrap.dedent(
        f"""\
        Can the following QUESTION be answered with the given CONTEXT?
        Answer YES or NO. Do not add any additional information.
        QUESTION:
        {question}
        CONTEXT:
        {contexts}
        """)
    response = llm_client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="gpt-4o")
    response = response.choices[0].message.content
    return response


def is_target_output_in_answer(
    answer: str,
    _,
    test_case: inductor.TestCase) -> str:
    """Evaluate if the target output is described in the answer.

    Intended to be used as a quality measure.

    Args:
        answer: Answer to evaluate.
        test_case: Test case which includes the target answer to
            evaluate the given answer against.
    
    Returns:
        An LLM response indicating if the target output is described in the
        answer.
    """
    target_answer = test_case.output

    # In the target answer, "INVALID", is shorthand used to indicate that the
    # question should not be answered. However, this quality measure should
    # still evaluate that the bot appropriately responded.
    if target_answer == "INVALID":
        target_answer = (
            "I'm a documentation Q&A bot, so I'm not able to respond to your "
            "question because it doesn't seem to be related to the source "
            "documents. OR Sorry, I do not know the answer to that question."
        )

    # The prompt uses "few-shot" prompting (i.e. providing examples of the
    # desired output in the prompt) in order to improve the accuracy of this
    # quality measure.
    prompt = textwrap.dedent(
        f"""\
        Is the following TARGET_OUTPUT described in the given ANSWER?
        OR if the TARGET_OUTPUT is code, is the code described in the given
        ANSWER functionally equivalent?
        OR if the QUESTION was sufficiently vague, is the ANSWER a valid
        response given the TARGET_OUTPUT?
        Answer YES or NO. Do not add any additional information.

        Example 1:
        QUESTION: Can I create a model without validation?
        TARGET_OUTPUT: The `model_construct()` method allows models to
        be created without validation.
        ANSWER: Yes, you can create a model without validation using the
        `model_construct()` method in Pydantic. This can be useful for cases
        such as when working with complex data already known to be valid, or
        when dealing with non-idempotent validator functions or validators with
        undesired side effects.
        YOUR RESPONSE: YES
        EXPLANATION: The entire TARGET_OUTPUT is described in the ANSWER.

        Example 2:
        QUESTION: What is ORM mode?
        TARGET_OUTPUT: ORM mode is now referred to as "arbitrary class
        instances". It allows Pydantic models to be created from arbitrary
        class instances by reading the instance attributes corresponding to
        the model field names. One common application of this functionality
        is integration with object-relational mappings (ORMs).
        ANSWER: ORM mode allows Pydantic models to be created from arbitrary
        class instances by reading the instance attributes corresponding to
        the model field names.
        YOUR RESPONSE: NO
        EXPLANATION: Only the first sentence of the TARGET_OUTPUT is described
        in the ANSWER.

        QUESTION:{test_case.inputs['question']}
        TARGET_OUTPUT:{target_answer}
        ANSWER:{answer}
        """)

    response = llm_client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="gpt-4o")
    response = response.choices[0].message.content
    return response


test_suite.add(
    inductor.QualityMeasure(
        name="can_question_be_answered_with_context",
        evaluator="LLM",
        evaluation_type="BINARY",
        spec=can_question_be_answered_with_context),
    inductor.QualityMeasure(
        name="is_target_output_in_answer",
        evaluator="LLM",
        evaluation_type="BINARY",
        spec=is_target_output_in_answer),
)


test_suite.add(
    inductor.HparamSpec(
        hparam_name="vector_query_text_type",
        hparam_type="SHORT_STRING",
        values=["rephrase", "original"]),
    inductor.HparamSpec(
        hparam_name="vector_query_result_num",
        hparam_type="NUMBER",
        values=[2, 4]),

    # To compare different prompts with this test suite, uncomment the
    # following lines and define the prompts in the prompts.py file.
    # inductor.HparamSpec(
    #     hparam_name="main_prompt",
    #     hparam_type="TEXT",
    #     values=[
    #         prompts.MAIN_PROMPT_DEFAULT,
    #         # prompts.MAIN_PROMPT_A,
    #         # prompts.MAIN_PROMPT_B,
    #     ]),
    # inductor.HparamSpec(
    #     hparam_name="rephrase_prompt",
    #     hparam_type="TEXT",
    #     values=[
    #         prompts.REPHRASE_PROMPT_DEFAULT,
    #         # prompts.REPHRASE_PROMPT_A
    #     ]),
)


if __name__ == "__main__":
    # Change the number of replicas and parallelize value as needed.
    # With the current configuration, the test suite will run with 8 test
    # cases, 2 hyperparameters with 2 values for each hyperparameter, and
    # 2 replicas. This results in 64 total executions (8 * 2 * 2 * 2 = 64).
    test_suite.run(replicas=2, parallelize=8)
