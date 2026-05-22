# Python CLI Chat

A simple terminal-based AI chat client built for the Hyperskill AI Engineer program.

This project uses the OpenAI Responses API to create a multi-turn command-line chat assistant. The assistant can respond to user messages, preserve conversation context, estimate request cost, and call a function to end the interaction when the user indicates they are done.

## Features

- Accepts user input from the terminal
- Sends user messages to the OpenAI Responses API
- Supports multi-turn conversation using `previous_response_id`
- Uses `gpt-5-nano` for low-cost responses
- Displays token usage after each request
- Estimates total request cost based on token usage
- Defines an `end_interaction` function tool
- Allows the assistant to call the function when the user wants to exit
- Prints the function call ID when the assistant calls the tool

## Tech Stack

- Python
- OpenAI Responses API
- OpenAI function tools
- python-dotenv

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd python-cli-chat
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

The `.env` file is ignored by Git and should not be committed.

## Usage

Run the CLI client:

```bash
python app.py
```

Enter a message when prompted:

```text
Enter a message: Tell me a fun fact about Python.
```

The assistant will respond in the terminal.

To end the conversation, say something like:

```text
I need to head out now.
```

The assistant should call the `end_interaction` function, and the program will print the function call ID before ending the session.

## Example Output

```text
Enter a message: Thanks, I gotta head out now.
You: Thanks, I gotta head out now.

Function call ID: call_jsSUHfjpecL5gUHVshlUrOo0
Ending interaction: User is heading out and ending the chat.
Tokens used: 1,140
Estimated cost: $0.00020680
```

## Cost Estimation

The app estimates cost using token usage returned by the API response.

For `gpt-5-nano`, the project uses a local pricing map with input, cached input, and output token rates. The displayed cost is an estimate and may differ from exact billing if pricing changes.

## Project Structure

```text
python-cli-chat/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Notes

This project demonstrates the basic structure of a tool-enabled CLI assistant:

```text
User input → OpenAI Responses API → Assistant response or function call → Local Python handling
```

The assistant decides when to call the `end_interaction` tool, but the local Python program executes the function and exits the loop.

## Disclaimer

This project is for educational purposes only.