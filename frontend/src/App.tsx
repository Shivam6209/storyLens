import React, { useState } from 'react';
import { QueryClient, QueryClientProvider, useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Toaster, toast } from 'react-hot-toast';
import FileUpload from './components/FileUpload';
import StoryCard from './components/StoryCard';
import { storyApi } from './services/api';
import type { UploadFormData, Story } from './types';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const StoryLensApp: React.FC = () => {
  const [showUpload, setShowUpload] = useState(true);
  const queryClient = useQueryClient();

  // Fetch stories
  const { data: stories = [], isLoading: storiesLoading, error: storiesError } = useQuery({
    queryKey: ['stories'],
    queryFn: () => storyApi.getStories(),
  });

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: (data: UploadFormData) => storyApi.uploadAndGenerate(data),
    onSuccess: (data) => {
      toast.success('Story generated successfully!');
      queryClient.invalidateQueries({ queryKey: ['stories'] });
      setShowUpload(false);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to generate story');
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: string) => storyApi.deleteStory(id),
    onSuccess: () => {
      toast.success('Story deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['stories'] });
    },
    onError: () => {
      toast.error('Failed to delete story');
    },
  });

  const handleUpload = (data: UploadFormData) => {
    uploadMutation.mutate(data);
  };

  const handleDelete = (id: string) => {
    deleteMutation.mutate(id);
  };

  const handleNewStory = () => {
    setShowUpload(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">StoryLens</h1>
              <p className="text-gray-600 mt-1">Transform your photos into creative stories</p>
            </div>
            {!showUpload && (
              <button
                onClick={handleNewStory}
                className="btn-primary"
              >
                Create New Story
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {showUpload ? (
          <div className="mb-8">
            <FileUpload 
              onUpload={handleUpload} 
              isLoading={uploadMutation.isPending}
            />
          </div>
        ) : null}

        {/* Stories Section */}
        <div className="mt-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Stories</h2>
            <span className="text-sm text-gray-500">
              {stories.length} {stories.length === 1 ? 'story' : 'stories'}
            </span>
          </div>

          {storiesLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="card animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                  <div className="space-y-2 mb-4">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                    <div className="h-4 bg-gray-200 rounded w-4/6"></div>
                  </div>
                  <div className="h-48 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : storiesError ? (
            <div className="text-center py-12">
              <p className="text-red-600">Failed to load stories. Please try again.</p>
            </div>
          ) : stories.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No stories yet</h3>
              <p className="text-gray-600 mb-4">Upload your first photo to create a story!</p>
              {!showUpload && (
                <button
                  onClick={handleNewStory}
                  className="btn-primary"
                >
                  Get Started
                </button>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {stories.map((story) => (
                <StoryCard
                  key={story.id}
                  story={story}
                  onDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>Powered by Microsoft Kosmos-2 and Coqui XTTS-v2</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <StoryLensApp />
    </QueryClientProvider>
  );
};

export default App;
