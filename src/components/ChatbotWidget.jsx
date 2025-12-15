import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatbotWidget.module.css';

export default function ChatbotWidget() {
  // Configuration
  const API_BASE_URL = 'http://localhost:8000';
  const CHAT_API_ENDPOINT = `${API_BASE_URL}/api/rag/query`;

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Hi! 👋 I\'m your AI assistant. Ask me anything about the Physical AI & Robotics textbook!',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call backend API with query as URL parameter
      const queryParams = new URLSearchParams({
        query_text: inputValue,
        student_id: sessionStorage.getItem('chatSessionId') || 'guest',
      });

      const response = await fetch(`${CHAT_API_ENDPOINT}?${queryParams.toString()}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.response_text,
        sources: data.sources,
        latency_ms: data.latency_ms,
        confidence_score: data.confidence_score,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: 'Sorry, Just Question book related ',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  return (
    <>
      {/* Floating Chat Button */}
      <button
        className={styles.chatButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Open chatbot"
        title="Ask me anything!"
      >
        <span className={styles.icon}>
          {isOpen ? '✕' : '💬'}
        </span>
      </button>

      {/* Chat Modal/Drawer */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className={styles.backdrop}
            onClick={() => setIsOpen(false)}
          />

          {/* Chat Panel */}
          <div className={styles.chatPanel}>
            {/* Header */}
            <div className={styles.header}>
              <div className={styles.headerContent}>
                <h3 className={styles.title}>🤖 AI Assistant</h3>
                <p className={styles.subtitle}>
                  Powered by Claude
                </p>
              </div>
              <button
                className={styles.closeButton}
                onClick={() => setIsOpen(false)}
                aria-label="Close chatbot"
              >
                ✕
              </button>
            </div>

            {/* Messages Container */}
            <div className={styles.messagesContainer}>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`${styles.message} ${styles[message.type]}`}
                >
                  <div className={styles.messageContent}>
                    <p className={styles.messageText}>{message.text}</p>

                    {/* Sources for bot messages */}
                    {message.type === 'bot' && message.sources && message.sources.length > 0 && (
                      <div className={styles.sources}>
                        <p className={styles.sourcesTitle}>📚 Sources:</p>
                        {message.sources.map((source, idx) => (
                          <div key={idx} className={styles.sourceItem}>
                            <strong>{source.title}</strong>
                            <br />
                            <small>
                              Relevance: {(source.similarity_score * 100).toFixed(0)}%
                            </small>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Latency info */}
                    {message.type === 'bot' && message.latency_ms && (
                      <div className={styles.latency}>
                        ⏱️ {message.latency_ms}ms
                      </div>
                    )}
                  </div>

                  <span className={styles.timestamp}>
                    {message.timestamp.toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                </div>
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <div className={`${styles.message} ${styles.bot}`}>
                  <div className={styles.messageContent}>
                    <div className={styles.typingIndicator}>
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <form className={styles.inputArea} onSubmit={sendMessage}>
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question..."
                className={styles.input}
                disabled={isLoading}
              />
              <button
                type="submit"
                className={styles.sendButton}
                disabled={isLoading || !inputValue.trim()}
                title="Send message (Enter)"
              >
                📤
              </button>
            </form>
          </div>
        </>
      )}
    </>
  );
}
