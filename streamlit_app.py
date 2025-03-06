import os
import time
import streamlit as st
from dotenv import load_dotenv
import sys

# Add the youtube-knowledge-assistant directory to the path
sys.path.append("youtube-knowledge-assistant")

# Load environment variables
load_dotenv()

# Force the vector database path to be "vector_db"
os.environ["VECTOR_DB_PATH"] = "vector_db"

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "db_path" not in st.session_state:
        # Always use the vector_db path
        st.session_state.db_path = "vector_db"
    if "creator_name" not in st.session_state:
        st.session_state.creator_name = "Creator"
    if "cache_hits" not in st.session_state:
        st.session_state.cache_hits = 0
    if "total_queries" not in st.session_state:
        st.session_state.total_queries = 0
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def build_sidebar():
    """Build the sidebar with configuration options."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/youtube-play.png", width=100)
        st.title("YouTube Knowledge Assistant")
        
        st.subheader("Configuration")
        
        # Database selection - force it to be vector_db
        db_path_input = st.text_input(
            "Vector Database Path", 
            value="vector_db",
            help="Path to the vector database directory"
        )
        # Always use vector_db regardless of user input
        st.session_state.db_path = "vector_db"
        if db_path_input != "vector_db":
            st.warning("Using 'vector_db' directory regardless of input")
        
        # Creator name input
        st.session_state.creator_name = st.text_input(
            "Creator Name", 
            value=st.session_state.creator_name,
            help="Name of the YouTube creator"
        )
        
        # Reset chat button
        if st.button("Reset Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.rag_chain = None
            st.session_state.cache_hits = 0
            st.session_state.total_queries = 0
            st.session_state.chat_history = []
            st.rerun()
        
        # Performance metrics
        if st.session_state.total_queries > 0:
            st.subheader("Performance")
            cache_hit_rate = (st.session_state.cache_hits / st.session_state.total_queries) * 100
            st.metric("Cache Hit Rate", f"{cache_hit_rate:.1f}%")
            st.caption(f"Cache hits: {st.session_state.cache_hits}/{st.session_state.total_queries} queries")
        
        # About section
        st.subheader("About")
        st.markdown(
            """
            This app allows you to chat with a YouTube creator based on their video content.
            
            The AI assistant responds in the style and with the knowledge of the creator.
            
            **How it works:**
            1. Transcripts are extracted from videos
            2. Content is processed and organized
            3. A vector database enables efficient retrieval
            4. RAG (Retrieval-Augmented Generation) powers the responses
            """
        )
        
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            st.error("⚠️ OPENAI_API_KEY is not set in the .env file")
        else:
            st.success("✓ OpenAI API key configured")
        
        # Check database path
        if not os.path.exists("vector_db"):
            st.error(f"⚠️ Vector database not found at: vector_db")
        else:
            st.success(f"✓ Vector database found")

def lazy_load_rag_chain():
    """Lazily load the RAG chain only when needed."""
    if st.session_state.rag_chain is None:
        with st.spinner(f"Building RAG chain for {st.session_state.creator_name}..."):
            try:
                from rag_chain import build_rag_chain
                start_time = time.time()
                
                # Create a wrapper around the rag_chain to track cache hits
                # Always use "vector_db" as the path
                original_rag_chain = build_rag_chain(
                    "vector_db", 
                    st.session_state.creator_name
                )
                
                # Define a wrapper function to track cache hits
                def rag_chain_with_tracking(input_text, chat_history=None):
                    from rag_chain import response_cache
                    
                    # Check if this would be a cache hit
                    import hashlib
                    cache_key = hashlib.md5(f"{input_text}|{str(chat_history[-3:] if chat_history else [])}".encode()).hexdigest()
                    is_cache_hit = cache_key in response_cache
                    
                    # Update stats
                    st.session_state.total_queries += 1
                    if is_cache_hit:
                        st.session_state.cache_hits += 1
                    
                    # Call the original chain
                    return original_rag_chain(input_text, chat_history)
                
                st.session_state.rag_chain = rag_chain_with_tracking
                
                elapsed_time = time.time() - start_time
                if st.session_state.rag_chain:
                    st.success(f"RAG chain built successfully in {elapsed_time:.2f} seconds!")
                else:
                    st.error("Failed to build RAG chain")
            except Exception as e:
                st.error(f"Error building RAG chain: {e}")
                return False
    return True

def display_chat_messages():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def process_user_input():
    """Process user input and generate a response."""
    if prompt := st.chat_input("Ask a question about the creator's content..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Load RAG chain if not already loaded
        if not lazy_load_rag_chain():
            return
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner(f"{st.session_state.creator_name} is thinking..."):
                try:
                    # Check if this is a cache hit
                    from rag_chain import response_cache
                    import hashlib
                    cache_key = hashlib.md5(f"{prompt}|{str(st.session_state.chat_history[-3:] if st.session_state.chat_history else [])}".encode()).hexdigest()
                    is_cache_hit = cache_key in response_cache
                    
                    # Generate response and measure time
                    start_time = time.time()
                    response = st.session_state.rag_chain(prompt, st.session_state.chat_history)
                    elapsed_time = time.time() - start_time
                    
                    # Display response
                    st.markdown(response)
                    
                    # Show performance info
                    if is_cache_hit:
                        st.caption(f"⚡ Response from cache in {elapsed_time:.2f} seconds")
                    else:
                        st.caption(f"Response generated in {elapsed_time:.2f} seconds")
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Update conversation history for context in future questions
                    st.session_state.chat_history.append((prompt, response))
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="YouTube Creator Chat",
        page_icon="🎬",
        layout="wide"
    )
    
    initialize_session_state()
    build_sidebar()
    
    # Main chat area
    st.title(f"💬 Chat with {st.session_state.creator_name}")
    st.markdown(f"Ask questions about {st.session_state.creator_name}'s content and get AI-powered responses based on their videos.")
    
    # Display chat history
    display_chat_messages()
    
    # Process user input
    process_user_input()

if __name__ == "__main__":
    main() 