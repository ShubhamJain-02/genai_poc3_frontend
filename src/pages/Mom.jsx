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
    if (file && file.type.startsWith('audio/')) {
      setAudioFile(file.name);
    }
  }, []);

  useEffect(() => {
    if (audioFile) {
      console.log('reached here', audioFile, typeof audioFile)
      processAudio();
    }
  }, [audioFile])


  const processAudio = async () => {
    if (!audioFile) return;

    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/process/', {
        path: audioFile
      });
      setResult(response.data.response);
      console.log(response.data.response)
    } catch (error) {
      console.error('Error processing audio:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
    <div className="container" id="get">
  <div className="card">
    <h3>Upload Files</h3>
    <div className="drop_box">
      <header>
        <h4>Select File here</h4>
      </header>
      <p>Files Supported: mp3, mp4, m4a, wav</p>
      <input type="file" onChange = {onChange} accept=".mp3,.mp4,.m4a, .wav" id="fileID"/>
    </div>

  </div>
</div>
</>
  )
}

export default Mom