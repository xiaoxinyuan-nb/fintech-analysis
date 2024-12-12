import React from 'react';
import { Card, Statistic } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { formatNumber } from '../utils/format';

interface Props {
  symbol: string;
  data?: {
    price: number;
    change: number;
    volume: number;
  };
}

export const RealtimeQuote: React.FC<Props> = ({ symbol, data }) => {
  if (!data) return null;

  const { price, change, volume } = data;
  const isPositive = change >= 0;

  return (
    <Card>
      <Statistic
        title={symbol}
        value={price}
        precision={2}
        valueStyle={{ color: isPositive ? '#3f8600' : '#cf1322' }}
        prefix={isPositive ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
        suffix="%"
      />
      <Statistic
        title="成交量"
        value={formatNumber(volume)}
        precision={0}
      />
    </Card>
  );
}; 