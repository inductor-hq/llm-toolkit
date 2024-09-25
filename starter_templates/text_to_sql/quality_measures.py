"""Quality Measures for Text to SQL LLM App."""

import textwrap
from typing import Any, Dict

import inductor
import openai

import database


openai_client = openai.OpenAI()


def compare_sql_results_equality(
    output: Dict[str, Any],
    _,
    test_case: inductor.TestCase
) -> bool:
    """Returns True if the output matches TestCase target output.

    Specifically, test that the output and target output are equal
    ignoring column naming and ordering within each row. 
    For example: [[col1, col2], [a, b]] will be considered equal to
    [[column2, column1], [b,a]]
    This is done because the LLM output SQL may not exactly match the
    target output column naming and ordering while still being
    considered correct.
    
    Args:
        output: The output of the LLM app as a dict containing
            the generated SQL and the results from executing the SQL.
        test_case: The inductor TestCase object with a correct SQL query
            that should generate similar results (only differing in
            column names/ordering) to the output of the LLM app's SQL query. 
    """
    # Output field names may not match exactly
    if output["valid_sql"]:
        output_vals = [set(x) for x in output["results"]]
        expected_sql = test_case.output
        _, values = database.get_sql_results_headers_and_values(expected_sql)
        expected_vals = [set(x) for x in values]
        return output_vals == expected_vals
    # For invalid test cases, test that the LLM app generated the expected response
    elif output["generated_sql"] == test_case.output:
        return True
    else:
        return False


def is_valid_sql_quality_measure(
    output: Dict[str, Any],
    _,
    test_case: inductor.TestCase
) -> bool:
    """Returns True if the output SQL is valid.
    
    Args:
        output: The output of the LLM app as a dict containing
            the generated and processed SQL and the results from
            executing the SQL.
    """
    # For invalid test cases, test that the bot generated the expected response
    if output["generated_sql"] == test_case.output:
        return True
    return database.is_valid_sql(output["processed_sql"])


def llm_compare_sql_results(
    output: Dict[str, Any],
    _,
    test_case: inductor.TestCase
) -> bool:
    """Returns True if the output mostly matches TestCase output.

    Often times the SQL results will be essentially the same, but
    slightly different in formatting (for instance putting just week
    number vs week number and year). For these cases, use an LLM to
    check and see if the results are essentially the same even if a
    few details are different that aren't relevant to the request.

    Args:
        output: The output of the LLM app as a dict containing
            the generated SQL and the results from executing the SQL.
        test_case: The inductor TestCase object with a correct SQL query
            that should generate similar results to the output of the
            LLM app's SQL query.
    """
    # Output field names may not match exactly
    if output["valid_sql"]:
        output_vals = [set(x) for x in output["results"]]
        expected_sql = test_case.output
        _, values = database.get_sql_results_headers_and_values(expected_sql)
        expected_vals = [set(x) for x in values]
    # For invalid test cases, test that the bot generated the expected response
    else:
        output_vals = output["generated_sql"]
        expected_vals = test_case.output
    request = test_case.inputs["analytics_text"]
    prompt = textwrap.dedent(f"""\
        You are evaluating a SQL generation tool. Given the following
        request:
        {request}
        with expected results of:
        {expected_vals}

        Do the following results answer the request and closely match
        the expected results except for some minor word choice differences:
        {output_vals}

        **Only output Yes or No and nothing else.**
    """)

    chat_completion = openai_client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="gpt-4o")
    return chat_completion.choices[0].message.content


def llm_readability(
    output: Dict[str, Any],
    _,
    test_case: inductor.TestCase
) -> str:
    """Evaluates the readability of the LLM program's output SQL.

    Args:
        output: Output of the LLM program.

    Returns:
        The readability between 1 and 5 of the SQL generated from the LLM.
    """
    # For invalid test cases, test that the bot generated the expected response
    if output["generated_sql"] == test_case.output:
        return "5"
    prompt = textwrap.dedent(f"""\
        What is the level of readability of the following SQL?
                
        {output["generated_sql"]}

        Note that the above code is intended to {output["input_text"]}.

        Rate readability on a scale of 1 through 5, where 1 means
        that the SQL's readability can easily be improved (e.g., by
        removing unnecessary fields), and 5 means that the SQL above is
        already highly readable (e.g., it is well-structured, concise,
        and uses common capitalization).

        **Only output the score as an integer and nothing else.**
    """)

    chat_completion = openai_client.chat.completions.create(
        messages=[{"role": "system", "content": prompt}],
        model="gpt-4o")
    return chat_completion.choices[0].message.content


TEXT_TO_SQL_QUALITY_MEASURES = [
    inductor.QualityMeasure(
        name="Correct Results",
        evaluator="FUNCTION",
        evaluation_type="BINARY",
        spec=compare_sql_results_equality
    ),
    inductor.QualityMeasure(
        name="Valid SQL Syntax for schema",
        evaluator="FUNCTION",
        evaluation_type="BINARY",
        spec=is_valid_sql_quality_measure
    ),
    inductor.QualityMeasure(
        name="LLM evaluator Correct Results",
        evaluator="LLM",
        evaluation_type="BINARY",
        spec=llm_compare_sql_results
    ),
    inductor.QualityMeasure(
        name="Readability",
        evaluator="HUMAN",
        evaluation_type="RATING_INT",
        spec=(
            "What is the level of readability of the generated SQL? "
            "(1 = readability could easily be improved, 5 = highly readable)")
    ),
    inductor.QualityMeasure(
        name="Readability (LLM-powered)",
        evaluator="LLM",
        evaluation_type="RATING_INT",
        spec=llm_readability
    )
]
