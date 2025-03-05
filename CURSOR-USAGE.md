# Using YouTube API in Cursor

This guide explains how to use the YouTube API directly from Cursor without needing to install or set up any additional tools.

## Option 1: Web Interface

The simplest way to interact with the YouTube API is through the HTML interface we've created:

1. Open the `youtube-mcp-interface.html` file in your browser
2. Enter your YouTube API key (get one from [Google Cloud Console](https://console.cloud.google.com/apis/credentials))
3. Select the action you want to perform:
   - Get video details
   - Search videos
   - Get channel details
   - Get video comments
4. Enter the required information and click "Submit"

This interface allows you to interact with the YouTube API directly from your browser without any additional setup.

## Option 2: JavaScript Script

If you prefer to use a script, you can use the `use-youtube-mcp.js` file:

1. Make sure you have Node.js installed
2. Create a `.env` file with your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```
3. Run the script:
   ```
   node use-youtube-mcp.js
   ```

This script demonstrates how to:
- Get video details
- Search for videos
- Get channel details
- Get video comments

## Getting a YouTube API Key

To use either option, you'll need a YouTube API key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create API credentials (API key)
5. Copy the API key for use in the interface or script

## Available Functions

The YouTube API provides many functions, including:

- **Video Information**:
  - Get video details (title, description, duration, etc.)
  - Get video statistics (views, likes, comments)
  - Search videos across YouTube

- **Channel Information**:
  - Get channel details
  - Get channel statistics
  - List channel videos

- **Comments**:
  - Get video comments
  - Get comment replies

- **Search**:
  - Search for videos by keyword
  - Filter search results

## Customizing the Code

Both the HTML interface and JavaScript script can be customized to add more functionality:

- Add more API endpoints
- Modify the UI
- Add more search filters
- Implement additional YouTube API features

## Troubleshooting

If you encounter issues:

1. Make sure your API key is correct
2. Check that you've enabled the YouTube Data API v3 in Google Cloud Console
3. Verify you haven't exceeded your API quota (free tier has limits)
4. Check the browser console or terminal for error messages 