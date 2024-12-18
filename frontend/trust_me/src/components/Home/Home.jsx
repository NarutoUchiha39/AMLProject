import React from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { message, Upload } from 'antd';
import { useState } from 'react';
const { Dragger } = Upload;


const Home = () => {
const [imageUrl, setImageUrl] = useState(null); 
const props = {
  name: 'file',
  multiple: false,
  action: 'http://127.0.0.1:5000/upload',
  onChange(info) {
    const { status } = info.file;
    if (status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (status === 'done') {
    
      console.log(info.file.response.image_url)
     setImageUrl(info.file.response.image_url)
      message.success(`${info.file.name} file uploaded successfully.`);

    } else if (status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  },
  onDrop(e) {
    console.log('Dropped files', e.dataTransfer.files);
  },
};
return(
    <div className="upload" style={{height:"50vh"}}>
        <Dragger {...props} style={{marginBottom:"2rem"}}>
            <p className="ant-upload-drag-icon">
            <InboxOutlined />
            </p>
            <p className="ant-upload-text">Click or drag file to this area to upload</p>
            <p className="ant-upload-hint">
            Support for a single upload. 
            </p>
        </Dragger>

        {imageUrl && (
        <div>
          <h3>Processed Image:</h3>
          <img src={`${imageUrl}`} alt="Processed result" style={{ maxWidth: '100%' }} />
        </div>
      )}
  </div>
)
};
export default Home;