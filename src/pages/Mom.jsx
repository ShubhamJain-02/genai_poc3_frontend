import React from 'react';
import './Mom.css';
import { useState, useCallback, useEffect } from 'react';
import axios from 'axios';

const Mom = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const onChange = useCallback((event) => {
    const file = event.target.files[0];
    console.log(file)
    setAudioFile(file);
  }, []);

  useEffect(() => {
    if (audioFile) {
      console.log(audioFile);
      processAudio();
    }
  }, [audioFile]);

  const processAudio = async () => {
    console.log(audioFile); // Debug log
    if (!audioFile) return;

    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', audioFile);

    // Debugging FormData
    console.log('FormData keys:', Array.from(formData.keys())); // Should output ['file']
    console.log('FormData values:', Array.from(formData.values()));

    try {
      const response = await axios.post('http://localhost:8000/process/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data); // Debug log
      setResult(response.data.response);
    } catch (error) {
      console.error('Error processing audio:', error); // Debug log
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container" id="get">
      <div className="card">
        <h3>Upload Files</h3>
        <div className="drop_box">
          <header>
            <h4>Select File here</h4>
          </header>
          <p>Files Supported: mp3, mp4, m4a, wav</p>
          <input type="file" onChange={onChange} accept=".mp3,.mp4,.m4a,.wav" id="fileID" />
        </div>
      </div>
    </div>
  );
};

export default Mom;
