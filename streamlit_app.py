import streamlit as st
import os
import subprocess
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="YouTube MCP Server",
    page_icon="🎬",
    layout="wide"
)

st.title("YouTube MCP Server")
st.markdown("A Model Context Protocol (MCP) server implementation for YouTube")

# Check for API key
api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your YouTube API Key:", type="password")
    if api_key:
        os.environ["YOUTUBE_API_KEY"] = api_key

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Video Search", "Channel Info", "Playlist Info", "Transcript"])

if page == "Home":
    st.markdown("""
    ## Features
    
    ### Video Information
    * Get video details (title, description, duration, etc.)
    * List channel videos
    * Get video statistics (views, likes, comments)
    * Search videos across YouTube

    ### Transcript Management
    * Retrieve video transcripts
    * Support for multiple languages
    * Get timestamped captions
    * Search within transcripts

    ### Channel Management
    * Get channel details
    * List channel playlists
    * Get channel statistics
    * Search within channel content

    ### Playlist Management
    * List playlist items
    * Get playlist details
    * Search within playlists
    * Get playlist video transcripts
    """)

elif page == "Video Search":
    st.header("Search YouTube Videos")
    
    query = st.text_input("Enter search term:")
    max_results = st.slider("Max results", 1, 50, 10)
    
    if st.button("Search") and query:
        with st.spinner("Searching..."):
            try:
                # This would call your MCP server in a real implementation
                st.info("In a complete implementation, this would call your YouTube MCP server")
                st.json({
                    "query": query,
                    "maxResults": max_results,
                    "results": [
                        {"title": "Example Video 1", "videoId": "example1"},
                        {"title": "Example Video 2", "videoId": "example2"}
                    ]
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif page == "Channel Info":
    st.header("Channel Information")
    
    channel_id = st.text_input("Enter Channel ID:")
    
    if st.button("Get Info") and channel_id:
        with st.spinner("Loading channel info..."):
            try:
                # This would call your MCP server in a real implementation
                st.info("In a complete implementation, this would call your YouTube MCP server")
                st.json({
                    "channelId": channel_id,
                    "title": "Example Channel",
                    "description": "This is an example channel",
                    "statistics": {
                        "viewCount": "1000000",
                        "subscriberCount": "10000"
                    }
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif page == "Playlist Info":
    st.header("Playlist Information")
    
    playlist_id = st.text_input("Enter Playlist ID:")
    
    if st.button("Get Playlist") and playlist_id:
        with st.spinner("Loading playlist info..."):
            try:
                # This would call your MCP server in a real implementation
                st.info("In a complete implementation, this would call your YouTube MCP server")
                st.json({
                    "playlistId": playlist_id,
                    "title": "Example Playlist",
                    "description": "This is an example playlist",
                    "items": [
                        {"title": "Playlist Video 1", "videoId": "example1"},
                        {"title": "Playlist Video 2", "videoId": "example2"}
                    ]
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif page == "Transcript":
    st.header("Video Transcript")
    
    video_id = st.text_input("Enter Video ID:")
    language = st.text_input("Language (optional, defaults to 'en'):", "en")
    
    if st.button("Get Transcript") and video_id:
        with st.spinner("Loading transcript..."):
            try:
                # This would call your MCP server in a real implementation
                st.info("In a complete implementation, this would call your YouTube MCP server")
                st.json({
                    "videoId": video_id,
                    "language": language,
                    "transcript": [
                        {"text": "This is the first caption", "start": 0.0, "duration": 2.0},
                        {"text": "This is the second caption", "start": 2.0, "duration": 2.5}
                    ]
                })
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("YouTube MCP Server - Powered by Model Context Protocol") 