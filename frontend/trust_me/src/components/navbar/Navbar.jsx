import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { Outlet } from 'react-router';
const { Header, Content, Footer } = Layout;

const Navbar = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  return (
    <Layout style={{height:"100vh",display:"flex",flexDirection:"column"}}>
      <Header
        style={{
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <div className="demo-logo" style={{color:"white",fontSize:"17px"}}> Skin Cancer Detection </div>
       
      </Header>
      <Content
        style={{
          padding: '0 48px',
          flex:1,
          display:"flex",
          flexDirection:"column",
          padding: 24,
        }}
      >
       
        <div
          style={{
            background: colorBgContainer,
            padding: 24,
            flex:1,
            borderRadius: borderRadiusLG,
          }}
        >
          <Outlet/>
        </div>
      </Content>
     
    </Layout>
  );
};
export default Navbar;