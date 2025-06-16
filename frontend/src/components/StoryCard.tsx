import React, { useState } from 'react';
import { PlayIcon, PauseIcon, TrashIcon, CalendarIcon } from '@heroicons/react/24/outline';
import type { StoryCardProps } from '../types';
import { storyApi } from '../services/api';

const StoryCard: React.FC<StoryCardProps> = ({ story, onDelete }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  const handlePlayPause = () => {
    if (!story.audio_url) return;

    if (!audio) {
      const newAudio = new Audio(story.audio_url);
      newAudio.addEventListener('ended', () => setIsPlaying(false));
      newAudio.addEventListener('error', () => {
        console.error('Audio playback error');
        setIsPlaying(false);
      });
      setAudio(newAudio);
      newAudio.play();
      setIsPlaying(true);
    } else {
      if (isPlaying) {
        audio.pause();
        setIsPlaying(false);
      } else {
        audio.play();
        setIsPlaying(true);
      }
    }
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this story?')) {
      onDelete?.(story.id);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="card hover:shadow-lg transition-shadow duration-200">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            story.story_type === 'poem' 
              ? 'bg-purple-100 text-purple-800' 
              : 'bg-blue-100 text-blue-800'
          }`}>
            {story.story_type === 'poem' ? '📝 Poem' : '📖 Story'}
          </span>
          <div className="flex items-center text-sm text-gray-500">
            <CalendarIcon className="h-4 w-4 mr-1" />
            {formatDate(story.created_at)}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {story.audio_url && (
            <button
              onClick={handlePlayPause}
              className="p-2 rounded-full bg-primary-100 text-primary-600 hover:bg-primary-200 transition-colors"
              title={isPlaying ? 'Pause audio' : 'Play audio'}
            >
              {isPlaying ? (
                <PauseIcon className="h-4 w-4" />
              ) : (
                <PlayIcon className="h-4 w-4" />
              )}
            </button>
          )}
          
          {onDelete && (
            <button
              onClick={handleDelete}
              className="p-2 rounded-full bg-red-100 text-red-600 hover:bg-red-200 transition-colors"
              title="Delete story"
            >
              <TrashIcon className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      <div className="prose prose-sm max-w-none">
        <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
          {story.story_text}
        </div>
      </div>

      {story.image_filename && (
        <div className="mt-4">
          <img
            src={storyApi.getImageUrl(story.image_filename)}
            alt="Story inspiration"
            className="w-full h-48 object-cover rounded-lg"
            loading="lazy"
          />
        </div>
      )}
    </div>
  );
};

export default StoryCard; 