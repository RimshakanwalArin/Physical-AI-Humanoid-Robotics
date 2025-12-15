import React from 'react';
import ChatbotWidget from '@site/src/components/ChatbotWidget';

/**
 * Root wrapper component that appears on every page
 * This is a special Docusaurus component that wraps the entire site
 */
export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatbotWidget />
    </>
  );
}
