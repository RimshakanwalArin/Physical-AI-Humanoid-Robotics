import React, { useEffect, useState } from 'react';

export default function SelectTextHandler() {
  const [selectedText, setSelectedText] = useState('');
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    document.addEventListener('mouseup', handleTextSelection);
    return () => document.removeEventListener('mouseup', handleTextSelection);
  }, []);

  const handleTextSelection = () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();

    if (text.length > 0) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      setSelectedText(text);
      setPosition({
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX
      });
      setShowButton(true);
    } else {
      setShowButton(false);
    }
  };

  const handleAskAI = () => {
    // Trigger chatbot with selected text
    const event = new CustomEvent('ask-ai', { detail: { text: selectedText } });
    document.dispatchEvent(event);
    setShowButton(false);
  };

  return showButton ? (
    <button
      className="ask-ai-button"
      onClick={handleAskAI}
      style={{
        position: 'absolute',
        top: `${position.top}px`,
        left: `${position.left}px`,
        zIndex: 1000
      }}
    >
      Ask AI
    </button>
  ) : null;
}
