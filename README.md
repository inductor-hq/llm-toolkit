# Inductor Open-Source LLM Toolkit

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Table of Contents

1. [LLM App Starter Templates](#llm-app-starter-templates)
2. [Features](#features)
3. [How to Get Started](#how-to-get-started)
4. [FAQ](#faq)

## LLM App Starter Templates

The Inductor LLM toolkit provides a set of LLM app starter templates (in the starter_templates/ directory), that make it easy for you to get started with rapidly prototyping an LLM application as well as a systematic, rapid development process for taking it from prototype to production.

We have released our first starter template, for a [documentation Q&A bot](starter_templates/documentation_qa/README.md). Each template provides an implementation of an LLM application tailored to a specific type of use case (e.g., documentation Q&A). Additionally, each template includes a comprehensive developer workflow that supports rapid prototyping and the tools needed to go from prototype to production. Both the application and the workflow are easily configurable to suit your specific requirements (e.g., to use your specific documentation in the case of documentation Q&A).

## Features

Designed to address the unique challenges of LLM application development, each template includes the necessary scaffolding to facilitate rapid prototyping as well as a systematic, rapid workflow to then go from prototype to production:

- **Application scaffolding**: A robust foundation for your LLM application, ensuring you have all the essential components to build upon.
- **Out-of-the-box UI for rapid prototyping**: With a single CLI command, you can start an auto-generated and securely shareable user interface that enables you to quickly prototype and gather feedback from stakeholders, via Inductor playgrounds.
- **Test suite scaffolding for easy evaluation-driven development**: Each template includes an Inductor test suite that can be customized for your particular use case.
- **Experimentation scaffolding for systematic improvement**: Each template includes built-in touchpoints for rapid and automated experimentation, which can be used with Inductor to automate and orchestrate testing of multiple different app variants in order to further improve your app.
- **Production logging integration for easy observability**: Pre-built logging integration to maintain visibility and monitor your application’s performance in a production environment.

## How to Get Started

To get started with the documentation Q&A bot starter template, see its [README file](starter_templates/documentation_qa/README.md) and follow the instructions therein to clone this repo, run the app, and start systematically developing your own LLM application.

## FAQ

#### Q: Do I need Inductor to run these templates?
A: No, you do not need Inductor to get started running major elements of this toolkit, such as the LLM application scaffolding of a starter template. However, using Inductor enables you to fully take advantage of the pre-built developer workflows included in each starter template (e.g., test suites and hyperparameters).

#### Q: How do I sign up for Inductor?
A: If you run the Inductor CLI, you will be prompted to log in to Inductor or create an account (for free) if you don't already have one.  Alternatively, if you don't already have an account, you can sign up [here](https://app.inductor.ai/signup).

#### Q: Where can I find more information about using Inductor?
A: Learn more about [Inductor](https://inductor.ai) by visiting our [documentation](https://app.inductor.ai/docs/index.html) or [booking a demo](https://inductor.ai/contact-us).

#### Q: Where can I request an addition to the toolkit?
A: You can request new features or report bugs by [filing an issue in this GitHub repo](https://github.com/inductor-hq/llm-toolkit/issues).

#### Q: Where can I ask any other questions?
A: Please [file an issue in this GitHub repo](https://github.com/inductor-hq/llm-toolkit/issues), [join our Slack community](https://join.slack.com/t/inductor-users/shared_invite/zt-2k1smhpbb-xCt_ZBkqkS4U8AP3Chj46Q), or email us at [support@inductor.ai](mailto:support@inductor.ai).  We're always happy to answer any questions!