import os
from flask import Flask, request, jsonify, render_template
from smolagents import CodeAgent, HfApiModel, DuckDuckGoSearchTool
from markdown_it import MarkdownIt

app = Flask(__name__)

# Initialize markdown-it
md = MarkdownIt()

# Retrieve the Hugging Face token from the environment variable
HF_TOKEN = os.environ.get('HF_TOKEN')
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set. Please set it before running the application.")

# Define the Hugging Face model through smolagents
model = HfApiModel(token=HF_TOKEN)

# Initialize the CodeAgent with the model and tools
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    max_steps=5
)

@app.route('/')
def home():
    return render_template('designAi.html')

@app.route('/design-assistant', methods=['POST'])
def design_assistant():
    question = request.form.get('question', '')
    prompt = f"""You are an AI Design Assistant specializing in collaborative design processes. Your role is to assist designers in generating, refining, and discussing design concepts and ideas.

When responding to queries or tasks, please:

1. Analyze the design challenge or question thoroughly.
2. Provide creative and practical suggestions, considering aesthetics, functionality, and user experience.
3. Offer multiple perspectives or solutions when appropriate.
4. Explain your reasoning and the principles behind your suggestions.
5. Ask clarifying questions if more information is needed to provide the best assistance.
6. Encourage collaboration by suggesting ways other team members could contribute or expand on ideas.
7. Consider sustainability, accessibility, and inclusivity in your design recommendations.
8. If relevant, reference current design trends or successful case studies.
9. Format your response for clarity, using bullet points or numbered lists when appropriate.

Remember, your goal is to inspire and facilitate creative collaboration among design team members.

Designer's input: {question}

Design Assistant's response:"""
    response = agent.run(prompt)
    return jsonify({'response': md.render(response)})

if __name__ == '__main__':
    app.run(debug=True)
