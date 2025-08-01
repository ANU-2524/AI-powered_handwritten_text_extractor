import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setExtractedText('');
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      setError('');
      const response = await axios.post('http://localhost:5000/extract', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setExtractedText(response.data.extracted_text);
    } catch (err) {
      console.error("Error:", err);
      setError('Error extracting text. Please make sure you are uploading a clear image or valid PDF.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h2>Upload Handwritten Image or PDF</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*,.pdf" onChange={handleFileChange} />
        <button type="submit" style={{ marginLeft: '1rem' }}>Extract</button>
      </form>

      {loading && <p>🔄 Extracting text...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {extractedText && (
        <div style={{ marginTop: '1.5rem' }}>
          <h3>📝 Extracted Text:</h3>
          <pre style={{ background: '#f5f5f5', padding: '1rem', whiteSpace: 'pre-wrap' }}>{extractedText}</pre>
        </div>
      )}
    </div>
  );
};

export default UploadForm;
