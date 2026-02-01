import streamlit as st
import uuid, os, json
import sys
from dotenv import load_dotenv

# Ensure we can import from src directories
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agent.agent import CustomerSupportAgent
from core.DBHandler import VectorDBManager

load_dotenv()

st.set_page_config("Customer Service Agent", page_icon="🤖")
st.title("📖 Customer Service Agent")

# --- INITIALIZATION ---
# Cache resources to prevent reloading on every run
@st.cache_resource
def get_db_manager():
    return VectorDBManager()

@st.cache_resource
def get_agent():
    return CustomerSupportAgent()


# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = [] 

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    print("Session ID : " + st.session_state.session_id)

# --- MESSAGE RENDERING ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
            if 'files_names' in message:
                for file_name in message['files_names']:
                    st.info(f"📄 {file_name}")

        else:  # assistant
            with st.container():
                # The assistant content is stored as [final_answer, step_details]
                if isinstance(message["content"], list) and len(message["content"]) >= 2:
                    final_ans = message["content"][0]
                    steps = message["content"][1]
                    
                    if steps:
                        with st.expander("Coding Steps"):
                            st.markdown(steps)
                    st.markdown(final_ans)
                else:
                    # Fallback for simple string content
                    st.markdown(message["content"])
            
# --- NEW USER INTERACTION ---
if user_text := st.chat_input("How can I help you?"):
    # 1. Update UI Message State
    st.session_state.messages.append({
        "role": "user", 
        "content": user_text
    })
    
    # 2. Update Agent History State (backend context)
    current_turn = {"role": "user", "content": user_text}
    st.session_state.history.append(current_turn)
    

    # Display immediately
    with st.chat_message("user"):
        st.markdown(user_text)

    # --- ASSISTANT RESPONSE ---
    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            with st.container():
                with st.expander("Coding Steps"):
                    step_placeholder = st.empty()
            final_answer_placeholder = st.empty()
            
            step_details = ""
            final_answer = ""
            counter = 1
            code_blocks = [] 
            
            try:
                # Instantiate Agent
                agent = get_agent()
                
                # Call agent as a generator
                generator = agent(
                    query=user_text,
                    history=st.session_state.history,
                    stream=True,
                    session_id=st.session_state.session_id
                )
                
                # Consume the generator
                for step_json in generator:
                    try:
                        data = json.loads(step_json)
                        resp_type = data.get("type")
                        resp_content = data.get("content")
                        
                        if resp_content:
                            if resp_type == "code":
                                step_details += f"**Step {counter}**\n\n{resp_content}\n---\n"
                                counter += 1
                                code_blocks.append(resp_content)
                                step_placeholder.markdown(step_details)
                            elif resp_type == "final":
                                final_answer = resp_content
                                final_answer_placeholder.markdown(final_answer)
                            # Handle other types if necessary
                            
                    except json.JSONDecodeError:
                        continue

            except Exception as e:
                st.error(f"Error executing agent: {e}")
                import traceback
                st.code(traceback.format_exc())

    # Save Assistant Response
    st.session_state.messages.append(
        {"role": "assistant", "content": [final_answer, step_details]})
    
    # Save to Compact History (for future context)
    if len(code_blocks) >= 2:
        st.session_state.history.append({
            "role": "assistant",
            "content": f"Before Last code block : \n{code_blocks[-2]}\n\nLast code block : \n{code_blocks[-1]}"
        })
    elif len(code_blocks) == 1:
        st.session_state.history.append({"role": "assistant", "content": code_blocks[-1]})
    else:
         st.session_state.history.append({"role": "assistant", "content": final_answer})
    
    st.rerun()
