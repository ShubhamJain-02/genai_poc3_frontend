import React from 'react';
import './Mom.css';

const Mom = () => {
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
      <input type="file" accept=".mp3,.mp4,.m4a, .wav" id="fileID"/>
    </div>

  </div>
</div>
</>
  )
}

export default Mom