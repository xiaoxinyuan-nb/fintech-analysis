import React from 'react';
import { Layout } from 'antd';
import Home from './pages/Home';
import './App.css';

const { Header, Content } = Layout;

const App: React.FC = () => {
  return (
    <Layout>
      <Header>
        <h1 style={{ color: 'white' }}>AI金融分析平台</h1>
      </Header>
      <Content style={{ padding: '24px' }}>
        <Home />
      </Content>
    </Layout>
  );
};

export default App; 