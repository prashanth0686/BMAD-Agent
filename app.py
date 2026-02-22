import streamlit as st
from google import genai
import os
import yaml
from dotenv import load_dotenv
from git import Repo  # Still used for repo initialization

# 1. Configuration & Paths
CONFIG_PATH = "core/config.yaml"
AGENT_PATH = "core/agents/bmad-master.md"
OUTPUT_DIR = "docs"

# 2. Load Local Secrets & Config
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def load_bmad_settings():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.error(f"Config not found at {CONFIG_PATH}.")
        return None

bmad_config = load_bmad_settings()
client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- NEW: Robust Git Automation ---
def git_commit_locally(file_path, message):
    """
    Directly invokes the Git CLI via GitPython to bypass OneDrive path errors.
    This is the 'fresh' approach that avoids index mapping bugs.
    """
    try:
        # 1. Initialize repo object
        repo = Repo(".", search_parent_directories=True)
        
        # 2. Use repo.git (the CLI wrapper) instead of repo.index (the high-level API)
        # This allows Git to handle the absolute path normalization itself.
        repo.git.add(file_path)
        repo.git.commit('-m', message)
        
        return True
    except Exception as e:
        st.error(f"Git Automation Error: {e}")
        return False

# --- UI Setup ---
st.set_page_config(page_title="BMAD Master Executor", page_icon="🧙", layout="wide")
st.title("🧙 BMAD Master Agent (Gemini 2.5 Flash)")

project_name = st.text_input("Project Name", placeholder="e.g., BMAD Sentinel")
user_brief = st.text_area("Project Brief", height=150)

def execute_bmad_task(task_label, task_instruction):
    if not user_brief:
        st.error("Please provide a project brief!")
        return

    with st.spinner(f"Generating {task_label}..."):
        with open(AGENT_PATH, 'r', encoding='utf-8') as f:
            bmad_rules = f.read()

        full_prompt = f"Role: {bmad_rules}\n\nTask: {task_instruction}\n\nProject: {project_name}\nBrief: {user_brief}"
        response = client.models.generate_content(model='gemini-2.5-flash', contents=full_prompt)
        content = response.text
        
        # Save locally
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_name = f"{project_name.replace(' ', '_')}_{task_label}.md"
        save_path = os.path.join(OUTPUT_DIR, file_name)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        st.success(f"File saved: {save_path}")
        return save_path

# --- UI Action Buttons ---
st.subheader("Workflow Actions")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Generate PRD"):
        execute_bmad_task("PRD", "Write a full PRD.")
with c2:
    if st.button("Generate User Stories"):
        execute_bmad_task("User_Stories", "Create User Stories.")
with c3:
    if st.button("Generate Test Cases"):
        execute_bmad_task("Test_Cases", "Produce Test Cases.")

# --- Interactive Chat with Intent Commit ---
st.divider()
st.subheader("💬 Chat with BMAD Master [CH]")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type /CH to chat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.startswith("/CH"):
        with st.chat_message("assistant"):
            chat_context = f"Project: {project_name}\nBrief: {user_brief}\n\nRequest: {prompt.replace('/CH', '').strip()}"
            response = client.models.generate_content(model='gemini-2.5-flash', contents=chat_context)
            
            assistant_response = response.text
            st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Commit logic triggered by chat
            if "commit" in prompt.lower():
                target_file = os.path.join(OUTPUT_DIR, f"{project_name.replace(' ', '_')}_PRD.md")
                if os.path.exists(target_file):
                    if git_commit_locally(target_file, f"feat: Automated commit of {project_name} PRD"):
                        st.info(f"✅ Committed {target_file} using Git CLI wrapper.")
                else:
                    st.warning("No PRD file found to commit.")

# Sidebar Explorer
st.sidebar.divider()
st.sidebar.subheader("Local Drafts")
if os.path.exists(OUTPUT_DIR):
    for file in os.listdir(OUTPUT_DIR):
        st.sidebar.text(f"📄 {file}")