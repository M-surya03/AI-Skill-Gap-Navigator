import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X, CheckCircle, Loader2 } from 'lucide-react';

interface ResumeUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  isAnalyzing: boolean;
}

const ResumeUpload: React.FC<ResumeUploadProps> = ({ onFileSelect, selectedFile, isAnalyzing }) => {
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    setError(null);
    if (rejectedFiles.length > 0) {
      setError('Invalid file type. Please upload a PDF, DOCX, or TXT file.');
      return;
    }
    if (acceptedFiles[0]) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled: isAnalyzing,
  });

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    onFileSelect(null as any);
    setError(null);
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  };

  if (selectedFile) {
    return (
      <div className="upload-zone" style={{ padding: '2rem', cursor: 'default' }}>
        <div className="flex items-center gap-4">
          <div
            className="section-icon section-icon-success"
            style={{ width: 56, height: 56, borderRadius: 12, flexShrink: 0 }}
          >
            <FileText size={24} color="var(--secondary-light)" />
          </div>
          <div className="flex-1" style={{ textAlign: 'left', minWidth: 0 }}>
            <div className="font-semibold" style={{ color: 'var(--text-primary)', fontSize: '0.95rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {selectedFile.name}
            </div>
            <div className="text-sm" style={{ color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              {formatSize(selectedFile.size)} · {selectedFile.type || 'document'}
            </div>
          </div>
          <div className="flex items-center gap-2">
            {isAnalyzing ? (
              <Loader2 size={20} style={{ color: 'var(--primary)', animation: 'spin 1s linear infinite' }} />
            ) : (
              <>
                <CheckCircle size={20} color="var(--secondary-light)" />
                <button
                  onClick={removeFile}
                  className="btn btn-sm btn-outline"
                  style={{ padding: '0.25rem', minWidth: 0, border: 'none' }}
                  title="Remove file"
                >
                  <X size={16} />
                </button>
              </>
            )}
          </div>
        </div>
        {isAnalyzing && (
          <div style={{ marginTop: '1rem' }}>
            <div className="flex justify-between text-xs mb-1" style={{ color: 'var(--text-muted)' }}>
              <span>Analyzing your resume…</span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill progress-fill-primary"
                style={{ width: '100%', animation: 'shimmer 1.5s infinite', backgroundSize: '200% 100%' }}
              />
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div>
      <div
        {...getRootProps()}
        className={`upload-zone ${isDragActive ? 'drag-over' : ''}`}
      >
        <input {...getInputProps()} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div
            className="animate-float"
            style={{
              width: 72, height: 72,
              background: 'rgba(99,102,241,0.15)',
              borderRadius: '50%',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 1.25rem',
              border: '2px solid var(--border-accent)',
            }}
          >
            <Upload size={32} color="var(--primary-light)" />
          </div>
          <h3 style={{ marginBottom: '0.5rem', fontSize: '1.1rem' }}>
            {isDragActive ? 'Drop your resume here' : 'Upload Your Resume'}
          </h3>
          <p className="text-secondary text-sm" style={{ marginBottom: '1.25rem' }}>
            Drag & drop or click to browse · PDF, DOCX, TXT · Max 10MB
          </p>
          <button className="btn btn-outline btn-sm" type="button" onClick={(e) => e.preventDefault()}>
            Browse Files
          </button>
        </div>
      </div>
      {error && (
        <p style={{ color: '#fca5a5', fontSize: '0.8rem', marginTop: '0.5rem' }}>
          ⚠ {error}
        </p>
      )}
    </div>
  );
};

export default ResumeUpload;
