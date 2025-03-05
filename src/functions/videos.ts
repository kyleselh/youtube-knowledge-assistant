import { google, youtube_v3 } from 'googleapis';

function safelyExecute<T>(fn: () => Promise<T>): Promise<T> {
  return fn().catch(error => {
    throw new Error(`Operation failed: ${error instanceof Error ? error.message : String(error)}`);
  });
}

export class VideoManagement {
  private youtube: youtube_v3.Youtube;

  constructor() {
    const apiKey = process.env.YOUTUBE_API_KEY;
    if (!apiKey) {
      throw new Error('YOUTUBE_API_KEY environment variable is not set. Please set it before running the application.');
    }

    this.youtube = new youtube_v3.Youtube({
      auth: apiKey
    });
  }

  async getVideo({ videoId, parts = ["snippet", "statistics", "contentDetails"] }: { videoId: string, parts?: string[] }) {
    return safelyExecute(async () => {
      const response = await this.youtube.videos.list({
        part: parts.join(','),
        id: videoId
      });
      
      return response.data.items?.[0] || null;
    });
  }

  // ... rest of the code ...
}