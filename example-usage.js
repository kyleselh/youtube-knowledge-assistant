// Example of using YouTube MCP programmatically
require('dotenv').config(); // Load environment variables from .env file

const { VideoManagement } = require('./src/functions/videos');

async function main() {
  try {
    // Initialize the video manager
    const videoManager = new VideoManagement();
    
    // Example: Get video details
    const videoId = 'dQw4w9WgXcQ'; // Rick Astley - Never Gonna Give You Up
    console.log(`Getting details for video: ${videoId}`);
    
    const videoDetails = await videoManager.getVideo({ 
      videoId,
      parts: ["snippet", "statistics", "contentDetails"]
    });
    
    console.log('\nVideo details:');
    console.log(JSON.stringify(videoDetails, null, 2));
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main(); 