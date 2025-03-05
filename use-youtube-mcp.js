// Self-contained script to use YouTube MCP directly from Cursor
// This script uses the existing YouTube MCP server you've already set up

// Load environment variables from .env file
require('dotenv').config();

// Import necessary modules
const { google } = require('googleapis');

// Simple implementation of video management functionality
class YouTubeAPI {
  constructor() {
    const apiKey = process.env.YOUTUBE_API_KEY;
    if (!apiKey) {
      throw new Error('YOUTUBE_API_KEY environment variable is not set. Please set it in your .env file.');
    }

    this.youtube = google.youtube({
      version: 'v3',
      auth: apiKey
    });
  }

  // Get video details
  async getVideoDetails(videoId) {
    try {
      const response = await this.youtube.videos.list({
        part: 'snippet,statistics,contentDetails',
        id: videoId
      });
      
      return response.data.items[0] || null;
    } catch (error) {
      console.error('Error fetching video details:', error.message);
      return null;
    }
  }

  // Search for videos
  async searchVideos(query, maxResults = 5) {
    try {
      const response = await this.youtube.search.list({
        part: 'snippet',
        q: query,
        maxResults: maxResults,
        type: 'video'
      });
      
      return response.data.items || [];
    } catch (error) {
      console.error('Error searching videos:', error.message);
      return [];
    }
  }

  // Get channel details
  async getChannelDetails(channelId) {
    try {
      const response = await this.youtube.channels.list({
        part: 'snippet,statistics,contentDetails',
        id: channelId
      });
      
      return response.data.items[0] || null;
    } catch (error) {
      console.error('Error fetching channel details:', error.message);
      return null;
    }
  }

  // Get video comments
  async getVideoComments(videoId, maxResults = 10) {
    try {
      const response = await this.youtube.commentThreads.list({
        part: 'snippet',
        videoId: videoId,
        maxResults: maxResults
      });
      
      return response.data.items || [];
    } catch (error) {
      console.error('Error fetching video comments:', error.message);
      return [];
    }
  }
}

// Main function to demonstrate usage
async function main() {
  try {
    console.log('Initializing YouTube API...');
    const youtubeAPI = new YouTubeAPI();
    
    // Example: Get video details
    const videoId = 'dQw4w9WgXcQ'; // Rick Astley - Never Gonna Give You Up
    console.log(`\nGetting details for video ID: ${videoId}`);
    
    const videoDetails = await youtubeAPI.getVideoDetails(videoId);
    if (videoDetails) {
      console.log('\nVideo Details:');
      console.log(`Title: ${videoDetails.snippet.title}`);
      console.log(`Channel: ${videoDetails.snippet.channelTitle}`);
      console.log(`Views: ${videoDetails.statistics.viewCount}`);
      console.log(`Likes: ${videoDetails.statistics.likeCount}`);
      console.log(`Comments: ${videoDetails.statistics.commentCount}`);
      console.log(`Duration: ${videoDetails.contentDetails.duration}`);
      console.log(`Published At: ${videoDetails.snippet.publishedAt}`);
    }
    
    // Example: Search for videos
    const searchQuery = 'programming tutorial';
    console.log(`\nSearching for videos with query: "${searchQuery}"`);
    
    const searchResults = await youtubeAPI.searchVideos(searchQuery, 3);
    if (searchResults.length > 0) {
      console.log('\nSearch Results:');
      searchResults.forEach((item, index) => {
        console.log(`\n${index + 1}. ${item.snippet.title}`);
        console.log(`   Channel: ${item.snippet.channelTitle}`);
        console.log(`   Published: ${item.snippet.publishedAt}`);
        console.log(`   Video ID: ${item.id.videoId}`);
      });
    }
    
    // Example: Get channel details from the first search result
    if (searchResults.length > 0) {
      const channelId = searchResults[0].snippet.channelId;
      console.log(`\nGetting details for channel ID: ${channelId}`);
      
      const channelDetails = await youtubeAPI.getChannelDetails(channelId);
      if (channelDetails) {
        console.log('\nChannel Details:');
        console.log(`Name: ${channelDetails.snippet.title}`);
        console.log(`Description: ${channelDetails.snippet.description.substring(0, 100)}...`);
        console.log(`Subscribers: ${channelDetails.statistics.subscriberCount}`);
        console.log(`Videos: ${channelDetails.statistics.videoCount}`);
        console.log(`Views: ${channelDetails.statistics.viewCount}`);
      }
    }
    
    // Example: Get video comments
    console.log(`\nGetting comments for video ID: ${videoId}`);
    
    const comments = await youtubeAPI.getVideoComments(videoId, 3);
    if (comments.length > 0) {
      console.log('\nTop Comments:');
      comments.forEach((item, index) => {
        const comment = item.snippet.topLevelComment.snippet;
        console.log(`\n${index + 1}. Author: ${comment.authorDisplayName}`);
        console.log(`   Comment: ${comment.textDisplay.substring(0, 100)}...`);
        console.log(`   Likes: ${comment.likeCount}`);
        console.log(`   Published: ${comment.publishedAt}`);
      });
    }
    
  } catch (error) {
    console.error('\nError occurred:');
    console.error(error.message);
  }
}

// Run the main function
main(); 