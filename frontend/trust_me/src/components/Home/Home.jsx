import React from 'react';
import { InboxOutlined } from '@ant-design/icons';
import { message, Table, Upload } from 'antd';
import { useState } from 'react';
const { Dragger } = Upload;


const Home = () => {
const [imageUrl, setImageUrl] = useState(null); 
const [dataSource,setDataSource] = useState(null)
const columns = [{
  title:'Model',
  dataIndex:'model',
  key:'model'
},

{
  title:'Accuracy',
  dataIndex:'accuracy',
  key:'accuracy'
},

{
  title:'Category',
  dataIndex:'category',
  key:'category'
},

]
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

      let resnet_prediction_category = info.file.response.predictions[0]
      let vgg19_prediction_category = info.file.response.predictions[1]

      let vgg19_confidence = info.file.response.confidence[0]
      let resnet_confidence = info.file.response.confidence[1]

      let dataSource = [
        {
          key:'1',
          model:'ResNet50',
          accuracy:resnet_confidence,
          category:resnet_prediction_category
        },

        {

          key:'2',
          model:'Vgg19',
          accuracy:vgg19_confidence,
          category:vgg19_prediction_category
        }
      ]
      console.log(dataSource)
      setDataSource(dataSource)
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
          {!imageUrl && <Dragger {...props} style={{marginBottom:"2rem"}}>
              <p className="ant-upload-drag-icon">
              <InboxOutlined />
              </p>
              <p className="ant-upload-text">Click or drag file to this area to upload</p>
              <p className="ant-upload-hint">
              Support for a single upload. 
              </p>
          </Dragger>
        }

        {imageUrl && (
        
        <div style={{display:'flex',justifyContent:"center",alignItems:"center"}}>
            <div style={{marginRight:"10rem"}}>
              <h3>Segmented Image:</h3>
              <img src={`${imageUrl}`} alt="Processed result" style={{ maxWidth: '100%' }} />
            </div>

            <Table
              columns={columns} dataSource={dataSource}
            />
        </div>
      )}
  </div>
)
};
export default Home;