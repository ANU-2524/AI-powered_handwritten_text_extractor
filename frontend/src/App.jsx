import { useState } from 'react';
import "./styles/App.css";

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setText('');
    setError('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await fetch("https://ai-powered-pu0r.onrender.com/extract", {
        method: "POST",
        body: formData
      });
      const data = await res.json();

      if (data.text) {
        setText(data.text);
      } else {
        setError(data.error || "Error extracting text.");
      }
    } catch (err) {
      setError("Server error or OCR failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🧠 AI Handwriting Extractor</h1>
      <h1>Upload Handwritten Image or PDF</h1>
      <input type="file" accept=".jpg,.jpeg,.png,.pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Extract</button>
      {loading && <p>Extracting...</p>}
      {error && <p className="error">{error}</p>}
      {text && (
        <>
          <h2>Extracted Text:</h2>
          <textarea readOnly value={text}></textarea>
        </>
      )}
    </div>
  );
}

export default App;
