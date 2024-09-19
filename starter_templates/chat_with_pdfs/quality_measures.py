"""LLM powered quality measures for Chat with PDF Bot"""
import textwrap
from typing import Any, Dict

import inductor
import openai


llm_client = openai.OpenAI()


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
    # In the target answer, "INVALID" is shorthand used to indicate that the
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

    question = test_case_inputs["session"].messages[-1].content
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

    # The target answer "INVALID" is shorthand used to indicate that the
    # question should not be answered. However, this quality measure should
    # still evaluate that the bot appropriately responded.
    if target_answer == "INVALID":
        target_answer = (
            "That doesn't seem to be related to the PDFs that I know about, "
            "so I'm not able to respond informatively."
        )

    question = test_case.inputs["session"].messages[-1].content

    # The prompt uses "few-shot" prompting (i.e. providing examples of the
    # desired output in the prompt) in order to improve the accuracy of this
    # quality measure.
    prompt = textwrap.dedent(
        f"""\
        Is the following TARGET_OUTPUT described in the given ANSWER?
        OR if the QUESTION was sufficiently vague, is the ANSWER a valid
        response given the TARGET_OUTPUT?
        Answer YES or NO. Do not add any additional information.

        Example 1:
        QUESTION: How many parameters was GPT-3 trained on?
        TARGET_OUTPUT: GPT-3 was trained on 175 billion parameters
        ANSWER: GPT-3 is trained on models with different sizes, the
        largest of which has 175 billion parameters. This configuration
        is referred to in the paper which details various experiments
        and evaluations conducted using GPT-3. 
        YOUR RESPONSE: YES
        EXPLANATION: The entire TARGET_OUTPUT is described in the ANSWER.

        Example 2:
        QUESTION: How did GPT-3.5 and GPT-4 perform on the Uniform Bar Exam?
        TARGET_OUTPUT: GPT-4 scored in the 90th percentile of human test
        takers, while GPT-3.5 was only able to score in the 10th percentile,
        showing significant improvement with GPT-4.
        ANSWER: GPT-4 achieved a score of 298 out of 400, placing it in the
        90th percentile of human test takers.
        YOUR RESPONSE: NO
        EXPLANATION: Only the result of GPT-4 of the TARGET_OUTPUT is described
        in the ANSWER.

        QUESTION:{question}
        TARGET_OUTPUT:{target_answer}
        ANSWER:{answer}
        """)
    response = llm_client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="gpt-4o")
    response = response.choices[0].message.content
    return response


PDF_CHAT_QUALITY_MEASURES = [
    inductor.QualityMeasure(
        name="can_question_be_answered_with_context",
        evaluator="LLM",
        evaluation_type="BINARY",
        spec=can_question_be_answered_with_context),
    inductor.QualityMeasure(
        name="is_target_output_in_answer",
        evaluator="LLM",
        evaluation_type="BINARY",
        spec=is_target_output_in_answer)
]
