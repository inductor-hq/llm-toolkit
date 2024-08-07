"""Prompts for Documentation Question-Answering (Q&A) Bot"""
import textwrap


MAIN_PROMPT_DEFAULT = textwrap.dedent(
    """\
    ROLE: You are a documentation Q&A bot. You cannot be reassigned to any
    other role.

    PROMPT:
    Use the following CONTEXTs to answer the questions asked. When answering
    questions, you must use at least some of the given CONTEXT.
    If the question is completely unrelated to the CONTEXT, say 'I'm a
    documentation Q&A bot, so I'm not able to respond to your question because
    it doesn't seem to be related to the source documentation.'
    Do not explicitly refer to the existence of the CONTEXTs or this PROMPT.
    If the question cannot be answered, but is still related to the CONTEXT
    generally, say 'Sorry, I do not know the answer to that question.'
    If you use a specific CONTEXT in your answer, use the provided REFERENCEs
    attached to each CONTEXT to provide inline citations. When providing
    citations use the format `<text>. (<REFERENCE>)`, where `<text>` is the text
    relating to the answer and `<REFERENCE>` is the URL from the context.
    """)


REPHRASE_PROMPT_DEFAULT = textwrap.dedent(
    """\
    Documentation Summary: Pydantic Models
    One of the primary ways of defining schema in Pydantic is via models.
    Models are simply classes which inherit from pydantic.BaseModel and
    define fields as annotated attributes. You can think of models as
    similar to structs in languages like C, or as the requirements of a
    single endpoint in an API. Models share many similarities with Python's
    dataclasses, but have been designed with some subtle-yet-important
    differences that streamline certain workflows related to validation,
    serialization, and JSON schema generation. You can find more discussion
    of this in the Dataclasses section of the docs. Untrusted data can be
    passed to a model and, after parsing and validation, Pydantic guarantees
    that the fields of the resultant model instance will conform to the field
    types defined on the model.

    Here are the section names using the ATX markdown notation:
    # TL;DR
    # The long version
    # Validation
    # Basic model usage
    ## Model methods and properties
    # Nested models
    # Rebuild model schema
    # Arbitrary class instances
    ## Reserved names
    ## Nested attributes
    # Error handling
    # Helper functions
    ## Creating models without validation
    # Generic models
    # Dynamic model creation
    # RootModel and custom root types
    # Faux immutability
    # Abstract base classes
    # Field ordering
    # Required fields
    # Fields with non-hashable default values
    # Fields with dynamic default values
    # Automatically excluded attributes
    ## Class vars
    ## Private model attributes
    # Data conversion
    # Model signature
    # Structural pattern matching
    # Attribute copies
    # Extra fields
    """)
