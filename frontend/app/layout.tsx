import type { ReactNode } from 'react';

export const metadata = {
  title: 'Bible Agent',
  description: 'Bible AI Agent MVP',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
