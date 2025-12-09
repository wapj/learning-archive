# OpenAI Agents SDK (Python) Learning Examples

This repository contains step-by-step examples to learn the `openai-agents-python` SDK, configured to use Google's Gemini models via `LiteLLM`.

## Prerequisites

1. **Install Python 3.10+**
2. **Install Dependencies**:
   ```bash
   pip install openai-agents litellm
   ```
3. **Get a Gemini API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/) and get an API key.
   - Export it in your terminal:
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```

## Examples

### 1. Basic Agent (`01_basic_agent.py`)
A simple agent that answers questions using Gemini 1.5 Flash.
- **Concepts**: `Agent`, `LitellmModel`, `Runner`.
- **Run**: `python 01_basic_agent.py`

### 2. Agent with Tools (`02_agent_with_tools.py`)
An agent equipped with a custom Python function (weather tool).
- **Concepts**: `@function_tool`, tool registration.
- **Run**: `python 02_agent_with_tools.py`

### 3. Structured Output (`03_structured_output.py`)
An agent that returns data in a specific Pydantic format (JSON).
- **Concepts**: Pydantic models, `output_type`.
- **Run**: `python 03_structured_output.py`

### 4. Interactive Chat (`04_interactive_agent.py`)
A command-line chat interface to talk to the agent.
- **Concepts**: Conversation history, interactive loops.
- **Run**: `python 04_interactive_agent.py`

### 5. Multi-Agent Handoff (`05_handoff_agents.py`)
A system of agents (Triage, Sales, Support) that transfer control to each other.
- **Concepts**: `handoffs`, `handoff_description`, multi-agent orchestration.
- **Run**: `python 05_handoff_agents.py`

## Troubleshooting
- If you see `AuthenticationError`, ensure your `GEMINI_API_KEY` is set correctly.
- If you see `Module not found`, ensure you are using the correct python environment where `openai-agents` is installed.
