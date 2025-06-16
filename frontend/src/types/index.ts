export interface Story {
  id: string;
  story_text: string;
  story_type: 'story' | 'poem';
  image_filename: string;
  audio_filename?: string;
  audio_url?: string;
  created_at: string;
  updated_at?: string;
}

export interface UploadResponse {
  id: string;
  story_text: string;
  story_type: string;
  image_filename: string;
  audio_filename?: string;
  audio_url?: string;
  created_at: string;
}

export interface ApiError {
  detail: string;
}

export interface UploadFormData {
  file: File;
  story_type: 'story' | 'poem';
}

export interface StoryCardProps {
  story: Story;
  onDelete?: (id: string) => void;
}

export interface AudioPlayerProps {
  audioUrl: string;
  title?: string;
}

export interface FileUploadProps {
  onUpload: (data: UploadFormData) => void;
  isLoading?: boolean;
} 