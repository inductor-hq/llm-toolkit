"""Test Suite for Chat with PDF Bot, Few-Shot... PDF"""
import inductor

import quality_measures
from test import pdf3_test_cases


test_suite = inductor.TestSuite(
    id_or_name="pdf_chat_pdf3",
    llm_program="app:chat_with_pdf")

test_suite.add(pdf3_test_cases.summary_test_cases)
test_suite.add(pdf3_test_cases.approach_test_cases)
test_suite.add(pdf3_test_cases.results_test_cases)

test_suite.add(quality_measures.PDF_CHAT_QUALITY_MEASURES)

# Uncomment the following lines to use Inductor hyperparameters.
# Be mindful that this will result in 16 (2*2*2*2) executions for
# each test case if all are used at once. This can result in
# non-trivial cost from your LLM provider
# test_suite.add(
#     inductor.HparamSpec(
#         hparam_name="query_filter_out_program_messages",
#         hparam_type="BOOLEAN"),
#     inductor.HparamSpec(
#         hparam_name="query_num_chat_messages",
#         hparam_type="NUMBER",
#         values=[5, 10]),
#     inductor.HparamSpec(
#         hparam_name="add_context_to_system_message",
#         hparam_type="BOOLEAN"),
#     inductor.HparamSpec(
#         hparam_name="query_result_num",
#         hparam_type="NUMBER",
#         values=[5, 10]),
# )


if __name__ == "__main__":
    # Change the number of replicas and parallelize value as needed.
    test_suite.run(replicas=1, parallelize=4)
