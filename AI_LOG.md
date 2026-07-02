# AI_LOG.md

# AI Assistance Log

## Introduction

AI was used as a programming assistant during the development of this project.

The generated code was reviewed, modified and tested manually before submission.

---

## Prompt 1

Read the project specification and summarize the required communication chain, command-line interface, output files and evaluation metrics.

### Result

AI summarized the required communication chain and identified the required modules including Source Encode, Scramble, Channel Encode, Frame Build, QPSK, Synchronization, Channel Decode and Metrics.

The generated summary was manually checked against the project specification.

---

## Prompt 2

Generate the project architecture and DESIGN.md.

### Result

AI generated a modular project structure including

main.py

source_codec.py

scrambler.py

channel_code.py

framing.py

modulation.py

channel.py

synchronization.py

metrics.py

plots.py

The design document was manually revised to match the project requirements.

---

## Prompt 3

Generate Python source code for every module in the src directory.

### Result

AI generated the initial implementation.

The generated functions were manually checked and modified.

Several interfaces were adjusted to satisfy the public tests.

---

## Prompt 4

Generate main.py.

### Result

AI generated a modular main program.

The final version only coordinates each module inside src.

All generated files are saved inside the results directory.

---

## Prompt 5

Analyze the public test failures reported by pytest.

### Result

AI identified several problems.

The source codec originally only supported file input.

The frame interface required too many parameters.

The synchronization interface did not support a custom preamble.

The documentation files lacked required keywords.

These problems were fixed manually after reviewing the generated suggestions.

---

## Prompt 6

Generate TEST_PLAN.md, MOCK_TEST_REPORT.md and AI_LOG.md.

### Result

AI generated the initial documents.

The contents were reorganized, simplified and manually revised before submission.

---

## Reflection

AI significantly improved development efficiency.

However, all generated code and documentation were reviewed manually.

The final implementation, debugging and testing were completed by the developer before submission.

## Adoption Reason

The final AI-generated suggestions were adopted because they matched the PRD requirements and made the code more modular.

The reason for adopting the modular structure is that `main.py` only controls the workflow, while each file in `src/` handles one communication function.

Some AI-generated content was not adopted directly. It was manually edited and changed because the public tests required more flexible function interfaces.

The final adoption decision was based on correctness, readability, and compatibility with public tests.