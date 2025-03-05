// Example of using YouTube MCP to download a video
require('dotenv').config();

const { VideoDownloader } = require('./src/functions/content/download');

async function downloadExample() {
  try {
    // Initialize the video downloader
    const downloader = new VideoDownloader();
    
    // Example: Download a video
    const videoId = 'dQw4w9WgXcQ'; // Rick Astley - Never Gonna Give You Up
    console.log(`Downloading video: ${videoId}`);
    
    // Download as MP4 (highest quality)
    const outputPath = await downloader.downloadVideo({ 
      videoId,
      format: 'mp4',
      quality: 'highest'
    });
    
    console.log(`Video downloaded to: ${outputPath}`);
    
    // Extract thumbnail at 30 seconds
    const thumbnailPath = await downloader.extractThumbnail({
      videoId,
      timestamp: 30
    });
    
    console.log(`Thumbnail extracted to: ${thumbnailPath}`);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

downloadExample(); 