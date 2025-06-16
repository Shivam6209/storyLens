import axios from 'axios';
import type { Story, UploadResponse, UploadFormData } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
});

export const storyApi = {
  // Upload image and generate story
  uploadAndGenerate: async (data: UploadFormData): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', data.file);
    formData.append('story_type', data.story_type);

    const response = await api.post<UploadResponse>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  // Get all stories
  getStories: async (skip = 0, limit = 100): Promise<Story[]> => {
    const response = await api.get<Story[]>('/stories', {
      params: { skip, limit },
    });
    return response.data;
  },

  // Get specific story
  getStory: async (id: string): Promise<Story> => {
    const response = await api.get<Story>(`/stories/${id}`);
    return response.data;
  },

  // Delete story
  deleteStory: async (id: string): Promise<void> => {
    await api.delete(`/stories/${id}`);
  },

  // Get audio file URL
  getAudioUrl: (filename: string): string => {
    return `${API_BASE_URL}/api/audio/${filename}`;
  },

  // Get image file URL
  getImageUrl: (filename: string): string => {
    return `${API_BASE_URL}/api/images/${filename}`;
  },
};

export default api; 