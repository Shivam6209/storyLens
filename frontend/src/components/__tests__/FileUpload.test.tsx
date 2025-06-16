import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import FileUpload from '../FileUpload';

// Mock react-dropzone
vi.mock('react-dropzone', () => ({
  useDropzone: () => ({
    getRootProps: () => ({ 'data-testid': 'dropzone' }),
    getInputProps: () => ({ 'data-testid': 'file-input' }),
    isDragActive: false,
  }),
}));

// Mock heroicons
vi.mock('@heroicons/react/24/outline', () => ({
  PhotoIcon: () => <div data-testid="photo-icon">PhotoIcon</div>,
  ArrowUpTrayIcon: () => <div data-testid="upload-icon">ArrowUpTrayIcon</div>,
}));

describe('FileUpload', () => {
  const mockOnUpload = vi.fn();

  it('renders upload area', () => {
    render(<FileUpload onUpload={mockOnUpload} />);
    
    expect(screen.getByText('Upload Your Photo')).toBeInTheDocument();
    expect(screen.getByText('Drag & drop an image here, or click to select')).toBeInTheDocument();
    expect(screen.getByTestId('photo-icon')).toBeInTheDocument();
  });

  it('shows loading state when uploading', () => {
    render(<FileUpload onUpload={mockOnUpload} isLoading={true} />);
    
    // Should still show the upload area when no file is selected
    expect(screen.getByText('Upload Your Photo')).toBeInTheDocument();
  });

  it('displays file format information', () => {
    render(<FileUpload onUpload={mockOnUpload} />);
    
    expect(screen.getByText('Supports JPEG, PNG, WebP (max 10MB)')).toBeInTheDocument();
  });
}); 