import { google } from 'googleapis';

async function start() {
    try {
        console.log('Starting YouTube MCP Server...');
        console.log('Environment check:');
        
        const apiKey = process.env.YOUTUBE_API_KEY;
        if (!apiKey) {
            console.error('ERROR: YOUTUBE_API_KEY environment variable is not set.');
            console.error('Please set your YouTube API key in the .env file or as an environment variable.');
            console.error('You can get a YouTube API key from https://console.cloud.google.com/apis/credentials');
            process.exit(1);
        }
        
        console.log('API Key:', 'Set ✓');
        console.log('\nYouTube MCP Server is ready to use!');
        console.log('You can now use this server with your MCP client.');
        
    } catch (error) {
        console.error('\nError occurred:');
        console.error(error.message);
        if (error.response) {
            console.error('\nAPI Response Error:');
            console.error(JSON.stringify(error.response.data, null, 2));
        }
    }
}

start();