import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { KLineChart } from '../components/KLineChart';
import { RealtimeQuote } from '../components/RealtimeQuote';
import { useWebSocket } from '../hooks/useWebSocket';
import { formatNumber } from '../utils/format';

const Home: React.FC = () => {
  const [quotes, setQuotes] = useState<any>({});
  
  // 订阅WebSocket数据
  const { data: realtimeData } = useWebSocket('realtime');
  const { data: klineData } = useWebSocket('kline');
  
  // 更新行情数据
  useEffect(() => {
    if (realtimeData) {
      setQuotes(prev => ({
        ...prev,
        [realtimeData.symbol]: realtimeData.data
      }));
    }
  }, [realtimeData]);

  return (
    <div className="home-page">
      <Row gutter={[16, 16]}>
        {/* 实时行情 */}
        <Col span={24}>
          <Card title="市场概览">
            <Row gutter={16}>
              {['SSE', 'SZSE', 'ChiNext'].map(symbol => (
                <Col span={8} key={symbol}>
                  <RealtimeQuote 
                    symbol={symbol}
                    data={quotes[symbol]}
                  />
                </Col>
              ))}
            </Row>
          </Card>
        </Col>

        {/* K线图表 */}
        <Col span={24}>
          <Card title="行情走势">
            <KLineChart data={klineData} />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Home; 