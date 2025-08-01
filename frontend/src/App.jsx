import React from 'react';
import UploadForm from './components/UploadForm';
import './styles/App.css';

function App() {
  return (
    <div className="App">
      <h1 style={{ textAlign: 'center', marginTop: '2rem' }}>🧠 AI Handwriting Text Extractor</h1>
      <UploadForm />
    </div>
  );
}

export default App;
