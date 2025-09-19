import os
from flask import Flask, request, jsonify, render_template
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool
from markdown_it import MarkdownIt
from werkzeug.utils import secure_filename
import base64


app = Flask(__name__)

# Initialize markdown-it
md = MarkdownIt()

# Retrieve the Hugging Face token from the environment variable
HF_TOKEN = os.environ.get('HF_TOKEN')
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set. Please set it before running the application.")

# Define the Hugging Face model through smolagents
model = InferenceClientModel(token=HF_TOKEN)

# Initialize the CodeAgent with the model and tools
agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    max_steps=5
)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('designAi.html')

@app.route('/design-feedback', methods=['POST'])
def design_feedback():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Convert image to base64 to pass into prompt
        with open(filepath, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

        prompt = f"""
You are an AI Design Assistant. The user has uploaded an image (encoded in base64) 
representing a design, sketch, or inspiration piece. Provide constructive design feedback, 
noting strengths, potential improvements, and alignment with modern design trends."""

        feedback = agent.run(prompt)
        return jsonify({"feedback": md.render(feedback)})
    else:
        return jsonify({"error": "Invalid file format"}), 400

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