import streamlit as st
import json
import os
import sys
from dotenv import load_dotenv


from services.pipeline import analyze_emails
from agents.assistant.agent import AssistantAgent
from agents.validator.agent import ValidatorAgent

load_dotenv()

st.set_page_config("Gestionnaire AI Workstation", page_icon="🏢", layout="wide")

# Initialize Session State
if "tickets" not in st.session_state:
    st.session_state.tickets = []
if "current_ticket_index" not in st.session_state:
    st.session_state.current_ticket_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = {} # Dict by ticket ID
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "draft_response" not in st.session_state:
    st.session_state.draft_response = ""
if "validation_report" not in st.session_state:
    st.session_state.validation_report = None
if "agent" not in st.session_state:
    st.session_state.agent = AssistantAgent()

# --- SIDEBAR & DISPATCHER ---
with st.sidebar:
    st.title("📬 Dispatcher")
    
    if not st.session_state.analyzed:
        if st.button("🔄 Analyze Incoming Emails", use_container_width=True, type="primary"):
            with st.spinner("Dispatching agents analyzing emails..."):
                tickets = analyze_emails()
                st.session_state.tickets = tickets
                st.session_state.analyzed = True
                st.rerun()
    
    if st.session_state.analyzed and st.session_state.tickets:
        st.subheader("Inbox")
        for idx, ticket in enumerate(st.session_state.tickets):
            urgency_icon = "🔴" if ticket.get('urgency') in ['high', 'critical'] else "🟢"
            dept = ticket.get('department', '').replace('_', ' ').title()
            # Show full subject, let Streamlit handle visual truncation if needed
            btn_label = f"{urgency_icon} [{dept}] {ticket.get('subject', 'No Subject')}"
            
            # Highlight selected
            type_btn = "primary" if idx == st.session_state.current_ticket_index else "secondary"
            
            if st.button(btn_label, key=f"ticket_{idx}", type=type_btn, use_container_width=True):
                st.session_state.current_ticket_index = idx
                st.rerun()
        
        if st.button("Reset / Refresh", use_container_width=True):
            st.session_state.analyzed = False
            st.session_state.tickets = []
            st.session_state.messages = {}
            st.rerun()

# --- MAIN CONTENT ---
if not st.session_state.analyzed:
    st.info("👋 Welcome to the Gestionnaire AI Workstation. Please analyze incoming emails to begin.")
    st.stop()

# Get Current Ticket
if not st.session_state.tickets:
    st.warning("No tickets found.")
    st.stop()

current_ticket = st.session_state.tickets[st.session_state.current_ticket_index]
ticket_id = current_ticket.get('id', str(st.session_state.current_ticket_index)) # Fallback ID

# Initialize chat history for this ticket if not exists
if ticket_id not in st.session_state.messages:
    # Auto-start with a summary request
    initial_summary_prompt = f"Summarize the case for this email:\nSubject: {current_ticket.get('subject')}\nBody: {current_ticket.get('body')}\nSender: {current_ticket.get('sender_id')}"
    st.session_state.messages[ticket_id] = [
        {"role": "user", "content": initial_summary_prompt, "hidden": True} # Hidden from view, triggers agent
    ]
    # We will trigger the run immediately below if it's the first message

# Layout: 2 Columns (Context vs Chat)
col_context, col_chat = st.columns([1, 2])

with col_context:
    st.subheader("Ticket Details")
    st.caption(f"**From:** {current_ticket.get('from')}")
    st.caption(f"**Subject:** {current_ticket.get('subject')}")
    st.caption(f"**Department:** {current_ticket.get('department')}")
    st.caption(f"**Urgency:** {current_ticket.get('urgency')}")
    
    with st.expander("📄 Email Body", expanded=True):
        st.markdown(current_ticket.get('body'))
    
    st.divider()
    
    st.subheader("📝 Response Draft")
    draft_area = st.text_area("Draft", value=st.session_state.draft_response, height=300)
    st.session_state.draft_response = draft_area
    
    if st.button("✅ Validate Draft with AI", use_container_width=True):
        with st.spinner("Validator Agent Checking..."):
            validator = ValidatorAgent()
            report = validator.validate(
                client_request=current_ticket.get('body'),
                client_context=f"Sender: {current_ticket.get('sender_id')}. Department: {current_ticket.get('department')}",
                draft_response=draft_area
            )
            st.session_state.validation_report = report
            
    if st.session_state.validation_report:
        with st.expander("Validation Report", expanded=True):
            st.markdown(st.session_state.validation_report)
            if st.button("💬 Copy to Chat", help="Copy report to chat history (does not trigger agent)"):
                st.session_state.messages[ticket_id].append({
                    "role": "user", 
                    "content": f"Here is the validation report:\n{st.session_state.validation_report}"
                })
                st.rerun()


with col_chat:
    st.subheader("💬 Assistant Chat")
    
    # Create a container for chat messages with fixed height and scroll
    chat_container = st.container(height=600)
    
    with chat_container:
        # Display History
        for idx, msg in enumerate(st.session_state.messages[ticket_id]):
            if not msg.get("hidden"):
                with st.chat_message(msg["role"]):
                    if msg["role"] == "assistant":
                        c1, c2 = st.columns([0.9, 0.1])
                        with c1:
                            if isinstance(msg["content"], list): # It's a complex response with steps
                                with st.expander("🕵️ Thinking Process"):
                                    st.markdown(msg["content"][1])
                                st.markdown(msg["content"][0])
                            else:
                                st.markdown(msg["content"])
                        with c2:
                            if st.button("📝", key=f"copy_draft_{idx}", help="Copy content to Draft Area"):
                                # Extract just the text content
                                text_content = msg["content"][0] if isinstance(msg["content"], list) else msg["content"]
                                st.session_state.draft_response = text_content
                                st.rerun()
                    else:
                        st.markdown(msg["content"])
        
        # Check if we need to run the auto-start summary (first hidden message)
        last_msg = st.session_state.messages[ticket_id][-1]
        if last_msg.get("hidden") and last_msg["role"] == "user":
            # Trigger Agent immediately for the summary
            with st.chat_message("assistant"):
                with st.spinner("Analyze du dossier en cours..."):
                    agent = st.session_state.agent
                    
                    # Setup streaming containers
                    step_placeholder = st.empty()
                    final_placeholder = st.empty()
                    
                    full_steps = ""
                    final_answer = ""
                    
                    # Stream the agent
                    for chunk_str in agent(query=last_msg["content"], stream=True):
                        try:
                            chunk = json.loads(chunk_str)
                            if chunk["type"] == "code": # Step update
                                full_steps += f"**Action:**\n```python\n{chunk['content']}\n```\n"
                                # We can render these in an expander if we want, or just log them
                                # For the summary, maybe just show thinking
                            elif chunk["type"] == "final":
                                final_answer = chunk["content"]
                                final_placeholder.markdown(final_answer)
                        except:
                            pass
                    
                    # Append to history
                    st.session_state.messages[ticket_id].append({
                        "role": "assistant",
                        "content": [final_answer, full_steps]
                    })
                    st.rerun()

    # User Input
    if prompt := st.chat_input("Ask about the case or request a draft..."):
        # Add User Message
        st.session_state.messages[ticket_id].append({"role": "user", "content": prompt})
        
        # Display User Message
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

            # Run Assistant
            with st.chat_message("assistant"):
                with st.spinner("Assistant is working..."):
                    agent = st.session_state.agent
                    
                    # Context building: Provide ONLY the last few messages to keep context window clean + Static Context
                    # For `smolagents`, we typically pass the query + history string or let it handle it.
                    # Here we will just pass the current prompt and rely on the agent's internal memory or pass conversation string
                    
                    # Let's construct a simple history string for the prompt context if needed, 
                    # but AssistantAgent.__call__ accepts `history`.
                    # We need to format history as a string or list as expected by your `agent.py` __call__
                    
                    # Simple string history for now
                    # We include ALL messages in the history passed to the LLM, including the hidden initial context
                    history_str = "\n".join([
                        f"{m['role'].upper()}: {m['content'][0] if isinstance(m['content'], list) else m['content']}" 
                        for m in st.session_state.messages[ticket_id]
                    ])
                    
                    # Containers
                    with st.expander("🕵️ Agent Actions"):
                        step_placeholder = st.empty()
                        
                    final_placeholder = st.empty()
                    
                    full_steps = ""
                    final_answer = ""
                    
                    # Execute
                    for chunk_str in agent(query=prompt, history=history_str, stream=True):
                        try:
                            chunk = json.loads(chunk_str)
                        except:
                            continue
                            
                        if chunk["type"] == "code":
                            # Append to steps
                            # chunk['content'] is tuple (code, "code") based on your parser
                            # Wait, your parser returns (str, "code")
                            # Actually look at your agent.py: `return f"\n```python\n{step.arguments}\n```\n\n", "code"`
                            # So it's already formatted markdow n
                            full_steps += chunk["content"]
                            step_placeholder.markdown(full_steps)
                            
                        elif chunk["type"] == "final":
                            final_answer = chunk["content"]
                            final_placeholder.markdown(final_answer)
                    
                    st.session_state.messages[ticket_id].append({
                        "role": "assistant",
                        "content": [final_answer, full_steps]
                    })
        st.rerun() # Rerun to update chat container properly with new messages
