# bedrock-claude-streamlit-chatbot-with-chat-history

A Streamlit-based chatbot leveraging Amazon Bedrock's Claude model for interactive, AI-driven conversations. It features chat history management and supports multiple simultaneous chat sessions, enabling persistent, context-aware interactions. Ideal for applications like customer support, educational tools, and personal assistants.

## Features

- **Multiple Chat Sessions**: Support for multiple simultaneous chat threads with separate contexts.
- **Chat History Management**: Saves conversation history to enable continuity in interactions.
- **Image Input Support**: Allows multiple image inputs within chat sessions.
- **Session Persistence**: Saves sessions with context and chat history as pickle files on your Windows machine.

## Prerequisites

- **Windows Machine**: The application is developed and tested on Windows.
- **AWS Account Access**: Requires login to your AWS account using `aws-azure-login`.

## Setup and Installation

1. **Login to AWS Account**:

   Open your command prompt and run:

   ```bash
   aws-azure-login --mode=gui
   ```

   This will open a GUI for you to authenticate and connect to your AWS account.

2. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/bedrock-claude-streamlit-chatbot-with-chat-history.git
   ```

3. **Navigate to the Project Directory**:

   ```bash
   cd bedrock-claude-streamlit-chatbot-with-chat-history
   ```

4. **Install Dependencies**:

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the Streamlit app using:

```bash
streamlit run st_multichat.py
```

This will launch the chatbot interface in your default web browser.

## Usage

- **Starting a New Chat Session**: You can initiate multiple chat sessions, each maintaining its own context and history.
- **Uploading Images**: Within any chat session, you can upload multiple images to enhance the interaction.
- **Session Management**: All sessions are saved as pickle files on your Windows machine, preserving the context and chat history for future use.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to enhance features or fix bugs.

## License

This project is licensed under the [MIT License](LICENSE).
