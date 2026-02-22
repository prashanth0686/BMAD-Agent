🧪 Testing the Agentic Workflow: BMAD Sentinel
This guide provides step-by-step instructions to run the BMAD Sentinel agent locally and test its "Automated Peer Reviewer" capabilities.

🚀 Local Execution
To start the web application, open your terminal in the project root folder and execute the following command:

Bash
python -m streamlit run app.py
🛠️ Example Test Case: The Peer Reviewer logic
Use the following inputs to test the agent’s ability to move beyond simple text generation into strategic analysis.

1. WebApp Inputs (Copy/Paste)
Project Name: BMAD Sentinel

Project Brief: Most PMs use AI to write docs. You are building an agent that critiques and improves them. It acts as an "Automated Peer Reviewer" that checks for logic gaps, technical debt, and edge cases before a developer ever sees the ticket.

2. Initial Generation
Click the "Generate PRD" button.

The Goal: Observe how the agent uses the BMAD structure to identify risks and technical constraints based on your brief.

3. Agentic Chat Refinement (The [CH] Command)
Once the initial document is generated, use the chat box at the bottom to test the agent's reasoning depth. Copy and paste this follow-up query:

/CH I like the risk analysis, but can you expand on the 'API Latency' section with a mitigation strategy?

🧠 Why this is "Agentic"
Unlike a standard chatbot, this workflow demonstrates:

Role Consistency: The agent maintains a "Senior PM Critic" persona throughout the session.

Contextual Memory: It uses your initial brief to provide specific technical mitigation strategies (like caching or asynchronous processing) rather than generic advice.

Autonomous Formatting: It automatically structures its findings into your local docs/ folder for immediate review.

📁 Troubleshooting
API Errors: Ensure your .env file contains a valid GEMINI_API_KEY.

Folder Issues: Ensure you have a folder named docs in your project root, or the app will attempt to create one on the first run.

OneDrive Conflicts: If you see "File not found" errors, ensure your terminal is pointed exactly at C:\Users\prash\OneDrive\Documents\GitHub\BMAD.
