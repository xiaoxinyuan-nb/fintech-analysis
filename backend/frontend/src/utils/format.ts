export const formatNumber = (num: number): string => {
  return new Intl.NumberFormat('zh-CN').format(num);
};

export const formatTime = (time: string): string => {
  return new Date(time).toLocaleString('zh-CN');
}; 