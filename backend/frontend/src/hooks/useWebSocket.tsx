import { useEffect, useState } from 'react';
import { message } from 'antd';

export const useWebSocket = (channel: string) => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/${channel}/SSE`);

    ws.onopen = () => {
      console.log(`Connected to ${channel} channel`);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setData(data);
      } catch (e) {
        setError('Failed to parse message');
      }
    };

    ws.onerror = (event) => {
      setError('WebSocket error');
      message.error('连接错误,请刷新页面重试');
    };

    ws.onclose = () => {
      console.log(`Disconnected from ${channel} channel`);
      // 可以在这里实现重连逻辑
    };

    return () => {
      ws.close();
    };
  }, [channel]);

  return { data, error };
}; 