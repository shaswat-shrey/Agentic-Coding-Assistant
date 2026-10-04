# Agentic Coding Assistant

> A tool-augmented autonomous software engineering agent powered by Google Gemini, capable of inspecting, modifying, executing, and iteratively debugging code inside a constrained sandboxed workspace.

---

## Overview

**Agentic Coding Assistant** is an LLM-driven software engineering agent that transforms natural-language programming objectives into executable multi-step workflows.

Unlike conventional LLM chat interfaces, the system is not limited to generating static code. The model can interact with a controlled filesystem and Python execution environment through structured function-calling interfaces.

The agent can:

- Inspect directories
- Discover files
- Read source code
- Create and modify files
- Execute Python programs
- Inspect execution results
- Reason over tool outputs
- Perform subsequent tool calls
- Iteratively solve multi-step programming tasks
- Produce a final natural-language response after completing the required operations

The architecture follows an **LLM → Tool Call → Deterministic Execution → Tool Result → LLM** feedback loop.

---

# System Architecture

```text
                           ┌─────────────────────┐
                           │       USER          │
                           │                     │
                           │ Natural Language    │
                           │ Programming Task    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │    Agent Runtime    │
                           │                     │
                           │ Context Management  │
                           │ Async Inference     │
                           │ Retry Handling      │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │     Gemini LLM      │
                           │                     │
                           │ Reasoning           │
                           │ Planning            │
                           │ Tool Selection      │
                           └──────────┬──────────┘
                                      │
                            Structured Function Call
                                      │
                                      ▼
              ┌─────────────────────────────────────────────┐
              │              Tool Orchestration             │
              │                                             │
              │  ┌───────────────────────────────────────┐  │
              │  │ get_files_info                        │  │
              │  │ get_file_content                      │  │
              │  │ write_file                            │  │
              │  │ run_python_file                       │  │
              │  └───────────────────────────────────────┘  │
              └──────────────────────┬──────────────────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │   Sandbox Boundary   │
                         │                      │
                         │     calculator/      │
                         │                      │
                         │ Filesystem           │
                         │ Python Runtime       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                              Tool Result
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Gemini Context    │
                         │                      │
                         │ Tool Result Analysis │
                         │ Next Action Planning │
                         └──────────┬───────────┘
                                    │
                                    ▼
                            More Tool Calls?
                              /          \
                            YES           NO
                             │             │
                             └──────┐      ▼
                                    │   Final Response
                                    │
                                    └──► Iterative Loop

The core execution model is an iterative Reason → Act → Observe → Reason loop.

                ┌─────────────────┐
                │  User Objective │
                └────────┬────────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ LLM Inference │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Tool Required?│
                 └───────┬───────┘
                    YES  │  NO
                         │
             ┌───────────┘
             ▼
       ┌──────────────┐
       │ Function Call│
       └───────┬──────┘
               │
               ▼
       ┌──────────────┐
       │ Tool Runtime │
       └───────┬──────┘
               │
               ▼
       ┌──────────────┐
       │ Tool Result  │
       └───────┬──────┘
               │
               ▼
       ┌──────────────┐
       │ Context Update│
       └───────┬──────┘
               │
               └──────────────► LLM
                                  │
                                  ▼
                             Next Action

Example:
"Find the bug in main.py, fix it, execute the program,
and verify that the output is correct."

The model can autonomously perform:

1. Read main.py
2. Analyze source
3. Identify defect
4. Write modified main.py
5. Execute main.py
6. Inspect stdout/stderr
7. Determine whether the fix worked
8. Iterate if necessary
9. Return final result
