# Design Agent for Collaborative Design Processes

## Introduction

This project implements a Design Agent using Flask and the smolagents library to create an AI-powered design assistant. The agent specializes in collaborative design processes, helping designers generate, refine, and discuss design concepts and ideas.

## Technologies Used

- **Flask**: For creating the web application
- **smolagents**: For integrating AI capabilities
- **Hugging Face API**: For natural language processing
- **DuckDuckGoSearchTool**: For real-time information retrieval
- **Markdown-it**: For rendering formatted responses

## Installation

1. Clone the repository.
2. Install the required dependencies:
  ```pip install flask smolagents markdown-it-py ddgs```
5. Set up your Hugging Face API token as an environment variable:   
   ```set HF_TOKEN=your_hugging_face_token_here```

## Usage

1. Run the Flask application: ```python designAgent.py```
2. Open a web browser and navigate to `http://localhost:5000`
3. Enter your design-related questions or challenges in the provided interface

## How It Works

The Design Agent uses a CodeAgent from the smolagents library, which is initialized with a DuckDuckGoSearchTool and a Hugging Face API model. When a user submits a question, the agent processes it through a carefully crafted prompt that guides its responses to be relevant, creative, and helpful for design processes.

## Examples

- **Design Concept Generation**: Users can input design challenges to receive innovative and practical suggestions.
- **Collaborative Design Discussion**: The agent encourages collaboration by suggesting ways team members can contribute or expand on ideas.

## Project Status

This project is open to contributions.

## Contributing

Contributions to improve the Design Agent are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

This project is open-source and available under the MIT License.
