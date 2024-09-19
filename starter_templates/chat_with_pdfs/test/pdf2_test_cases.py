"""Test Cases for Chat with PDF Bot, GPT-4... PDF"""
import textwrap

import inductor


# Summary Test cases
summary_chat_messages = [
    inductor.ChatMessage(
        role="user",
        content="Tell me the titles of all the PDFs you know about"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """\
            The titles of the PDFs I know about: 1. "Attention Is All You 
            Need" (<https://arxiv.org/pdf/1706.03762>) 2. "Language Models
            are Few-Shot Learners" (<https://arxiv.org/pdf/2005.14165>)
            3. "GPT-4 Technical Report" (<https://arxiv.org/pdf/2303.08774>)
            If you need more detailed information from any of these
            documents, please let me know!"
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="Can you provide a short summary of the GPT-4 paper"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            The GPT-4 Technical Report discusses the capabilities,
            limitations, and societal impacts of the GPT-4 language
            model. It highlights the model's enhancements over previous
            versions, including improved performance in natural language
            processing tasks and standardized tests like the Uniform Bar
            Exam. The paper also examines GPT-4's utility in various
            applications such as content generation, translation,
            and visual inputs, while addressing potential risks like
            the generation of harmful content and ethical considerations.
            Efforts to mitigate these risks through safety testing,
            fine-tuning, and ongoing research are emphasized.
            (https://arxiv.org/pdf/2303.08774)"
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="How well does GPT-4 do with visual inputs"
    ),
]


summary_test_cases = [
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=summary_chat_messages[:1]
            )
        },
        target_output=summary_chat_messages[1]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=summary_chat_messages[:3]
            )
        },
        target_output=summary_chat_messages[3]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=summary_chat_messages
            )
        },
        target_output=textwrap.dedent(
            """\
            Over a range of domains – including documents with text
            and photographs, diagrams, or screenshots – GPT-4 exhibits
            similar capabilities as it does on text-only inputs.
            """
        )
    ),
]


# Results Questions:
results_chat_messages = [
    inductor.ChatMessage(
        role="user",
        content=("How does the performance of GPT-4 compare "
                 "to previous models")
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            GPT 4 improves upon previous models such as GPT 3.5
            across various metrics:

            Reduction in Hallucinations: It scores 19 percentage
            points higher than the latest GPT-3.5 on internal,
            adversarially-designed factuality evaluations
            (https://arxiv.org/pdf/2303.08774)

            TruthfulQA Benchmark: GPT-4 significantly outperforms
            GPT-3.5 and other models in both zero-shot and few-shot
            prompting scenarios (https://arxiv.org/pdf/2303.08774)

            Exam Performance: When tested on a set of diverse benchmarks,
            including exams designed for humans, GPT-4's performance was
            evaluated using a refined methodology, often outperforming
            previous models. The exams included both multiple-choice
            and free-response questions, and GPT-4 was evaluated without
            specialized training for these exams.
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="What specific exams was GPT-4 tested on"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            "GPT-4 was tested on a diverse set of professional and
            academic exams. Some of the specific exams included are:
            1. **Uniform Bar Exam**: GPT-4 achieved a score in the top
            10% of test-takers.
            2. **AP Exams**: - AP Biology - AP Macroeconomics
            - AP US History - AP Art History - AP Statistics
            - AP Environmental Science - AP English Literature
            - AP US Government - AP Chemistry - AP World History
            - AP Psychology - AP Physics 2 - AP English Language
            - AP Microeconomics - AP Calculus BC
            3. **SAT**: - SAT Math
            - SAT EBRW (Evidence-Based Reading and Writing)
            4. **GRE**: - GRE Verbal - GRE Quantitative
            5. **LSAT**: Law School Admission Test.
            6. **AMC 10** and **AMC 12**: American Mathematics Competitions.
            7. **USABO Semifinal**: USA Biology Olympiad.
            8. **Codeforces**: Competitive programming contests.
            
            The exams included both multiple-choice and free-response
            questions, with scoring calibrated to simulate real exam
            conditions and reported using corresponding rubrics and
            percentiles. (https://arxiv.org/pdf/2303.08774)"
            """)
    ),
    inductor.ChatMessage(
        role="user",
        content="How did GPT-3.5 score on the Bar exam test"
    ),
    inductor.ChatMessage(
        role="program",
        content="GPT-3.5 scored in the 10th percentile among test takers"
    ),
    inductor.ChatMessage(
        role="user",
        content="How did GPT-4 and GPT-3.5 perform on the SAT tests"
    )
]


results_test_cases = [
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=results_chat_messages[:1]
            )
        },
        target_output=results_chat_messages[1]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=results_chat_messages[:3]
            )
        },
        target_output=results_chat_messages[3]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=results_chat_messages[:5]
            )
        },
        target_output=results_chat_messages[5]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=results_chat_messages
            )
        },
        target_output=textwrap.dedent(
            """\
            1. **SAT Evidence-Based Reading & Writing (EBRW)**:
            - **GPT-4**: 710 out of 800, approximately the 93rd percentile.
            - **GPT-3.5**: 670 out of 800, approximately the 87th percentil
            2. **SAT Math**: - **GPT-4**: 700 out of 800, approximately the
            89th percentile.
            - **GPT-3.5**: 590 out of 800, approximately the 70th percentile.
            """
        )
    ),
]


# Safety Questions
safety_chat_messages = [
    inductor.ChatMessage(
        role="user",
        content=("How was GPT-4 ensured to be safe")
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            GPT-4 makes significant improvements in safety over previous
            models by using:
            1. **Adversarial Testing via Domain Experts**:
            We engaged over 50 experts from domains such as long-term
            AI alignment risks, cybersecurity, biorisk, and
            international security to adversarially test the model.
            2. **Model-Assisted Safety Pipeline**:
            The pipeline uses models themselves as tools and consists of
            two main components, an additional set of safety-relevant RLHF
            training prompts, and rule-based reward models (RBRMs).
            (https://arxiv.org/pdf/2303.08774)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content=("What were the results of these safety measures "
                 "in comparision to GPT-3.5")
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            Our mitigations have significantly improved many of GPT-4’s
            safety properties. We’ve decreased the model’s tendency to
            respond to requests for disallowed content (Table 6) by 82%
            compared to GPT-3.5, and GPT-4 responds to sensitive requests
            (e.g., medical advice and self-harm, Table 7) in accordance
            with our policies 29% more often (Figure 9). On the
            RealToxicityPrompts dataset [73], GPT-4 produces toxic
            generations only 0.73% of the time, while
            GPT-3.5 generates toxic content 6.48% of time.
            (https://arxiv.org/pdf/2303.08774)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="Can you explain how the rule-based reward models work"
    )
]


safety_test_cases = [
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=safety_chat_messages[:1]
            )
        },
        target_output=safety_chat_messages[1]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=safety_chat_messages[:3]
            )
        },
        target_output=safety_chat_messages[3]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=safety_chat_messages
            )
        },
        target_output=textwrap.dedent(
            """\
            Our rule-based reward models (RBRMs) are a set of zero-shot GPT-4
            classifiers. These classifiers provide an additional reward signal
            to the GPT-4 policy model during RLHF fine-tuning that targets
            correct behavior, such as refusing to generate harmful content or
            not refusing innocuous requests.
            The RBRM takes three inputs: the prompt (optional), the output from
            the policy model, and a human-written rubric (e.g., a set of rules
            in multiple-choice style) for how this output should be evaluated.
            Then, the RBRM classifies the output based on the rubric. We can
            reward GPT-4 for refusing these requests. Conversely, we can reward
            GPT-4 for not refusing requests on a subset of prompts guaranteed
            to be safe and answerable. (https://arxiv.org/pdf/2303.08774)
            """
        )
    ),
]
