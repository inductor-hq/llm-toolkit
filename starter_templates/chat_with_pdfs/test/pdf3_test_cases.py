"""Test Cases for Chat with PDF Bot, Few-Shot... PDF"""
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
        content=("Can you provide a short summary of the Language Models "
                 "are Few-Shot Learners paper")
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            The paper "Language Models are Few-Shot Learners" focuses
            on GPT-3, an autoregressive language model with 175 billion
            parameters. It explores the effects of training on larger
            datasets with few shot, one shot, or zero shot methodologies.
            It compares the results of GPT-3 to state of the
            art fine tuned NLP models.
            (<https://arxiv.org/pdf/2005.14165>)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="What are the main sections outlined in this paper"
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
            1 Introduction
            2 Approach
            3 Results
            4 Measuring and Preventing Memorization Of Benchmarks
            5 Limitations
            6 Broader Impacts
            7 Related Work
            8 Conclusion
            (<https://arxiv.org/pdf/2005.14165>)
            """
        )
    ),
]


# Approach Test cases
approach_chat_messages = [
    inductor.ChatMessage(
        role="user",
        content=("What is the difference between few-shot, one-shot "
                 "and zero-shot")
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """\
            Few-shot, one-shot, and zero-shot refer to different evaluation
            settings for language models, particularly in terms of how much
            task-specific information is provided at inference time.
            1. **Few-Shot (FS)**: In few-shot learning, the model is given a
            few demonstrations of the task at inference time as conditioning,
            but no weight updates are allowed.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            2. **One-Shot (1S)**: One-shot learning is similar to few-shot
            learning, but only one demonstration is provided. Additionally,
            a natural language description of the task is given.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            3. **Zero-Shot (ZS)**: In zero-shot learning, the model is given
            no task-specific examples during inference time. Instead, it relies
            solely on its pre-trained knowledge and any natural language
            description of the task.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="What datasets are used in training GPT-3"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            The datasets used are:
            - Common Crawl (filtered)
            - Webtext2
            - Books1
            - Books2
            - English language Wikipedia
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="Was GPT-3 trained on the full text of the datasets"
    ),
]


approach_test_cases = [
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=approach_chat_messages[:1]
            )
        },
        target_output=approach_chat_messages[1]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=approach_chat_messages[:3]
            )
        },
        target_output=approach_chat_messages[3]
    ),
    inductor.TestCase(
        inputs={
            "session": inductor.ChatSession(
                messages=approach_chat_messages
            )
        },
        target_output=textwrap.dedent(
            """\
            The training datasets were sampled. This sampling is not
            done in proportion to the datasets overall size, but
            rather datasets viewed as higher quality.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
]


# Results:
results_chat_messages = [
    inductor.ChatMessage(
        role="user",
        content="What categories of tasks was GPT-3 evaluated on"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """\
            - Language Modeling, Cloze, and Completion Tasks
            - Closed Book Question Answering
            - Translate languages
            - Winograd-Style Tasks
            - Common sense reasoning
            - Reading Comprehension
            - SuperGLUE Benchmark
            - Natural Language Inference
            - Tasks designed especially to probe in-context learning abilities
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="What are winograd-style tasks"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            Winograd-style tasks involve determining which word a pronoun
            refers to, when the pronoun is grammatically ambiguous but
            semantically unambiguous to a human.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="How scores did GPT-3 achieve on Winograd-style tasks"
    ),
    inductor.ChatMessage(
        role="program",
        content=textwrap.dedent(
            """
            On Winograd GPT-3 achieves 88.3%, 89.7%, and 88.6% in
            the zero-shot, one-shot, and few-shot settings, showing
            no clear in-context learning but in all cases achieving
            strong results just a few points below state-of-the-art
            and estimated human performance.
            On the more difficult Winogrande dataset, we do find gains
            to in-context learning: GPT-3 achieves 70.2% in the
            zero-shot setting, 73.2% in the one-shot setting,
            and 77.7% in the few-shot setting.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
    inductor.ChatMessage(
        role="user",
        content="How does that compare to other models and human performance"
    ),
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
            The RoBERTA model achieves 79%, state-of-the-art is 84.6% achieved
            with a fine-tuned high capacity model (T5), and
            human performance on the task as reported by [SBBC19] is 94.0%.
            (REFERENCE: https://arxiv.org/pdf/2005.14165)
            """
        )
    ),
]
