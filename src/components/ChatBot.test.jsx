import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatBot from './ChatBot';

// Mock fetch
global.fetch = jest.fn();

describe('ChatBot Component', () => {
  beforeEach(() => {
    fetch.mockClear();
    localStorage.clear();
  });

  test('renders chatbot container', () => {
    render(<ChatBot />);
    const container = document.querySelector('.chatbot-container');
    expect(container).toBeInTheDocument();
  });

  test('displays input field and send button', () => {
    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    const button = screen.getByRole('button', { name: 'Send' });

    expect(input).toBeInTheDocument();
    expect(button).toBeInTheDocument();
  });

  test('handles form submission', async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({
        answer: 'Test answer',
        sources: [],
        latency_ms: 100,
      }),
    });

    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    const button = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'What is robotics?' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText('Test answer')).toBeInTheDocument();
    });
  });

  test('displays sources when provided', async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({
        answer: 'Answer text',
        sources: [
          {
            chapter_title: 'Introduction',
            section_title: 'Basics',
            excerpt: 'Sample text',
          },
        ],
        latency_ms: 100,
      }),
    });

    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    fireEvent.change(input, { target: { value: 'Test question' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    await waitFor(() => {
      expect(screen.getByText('Introduction')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    await waitFor(() => {
      expect(
        screen.getByText(
          'Chat service temporarily unavailable. Please try again.'
        )
      ).toBeInTheDocument();
    });
  });

  test('stores session ID in localStorage', () => {
    render(<ChatBot />);
    const sessionId = localStorage.getItem('session_id');
    expect(sessionId).toBeTruthy();
    expect(sessionId).toMatch(
      /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
    );
  });

  test('reuses session ID from localStorage', () => {
    const testSessionId = 'test-session-123';
    localStorage.setItem('session_id', testSessionId);

    fetch.mockResolvedValueOnce({
      json: async () => ({
        answer: 'Test',
        sources: [],
        latency_ms: 0,
      }),
    });

    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/chat'),
      expect.objectContaining({
        body: expect.stringContaining(testSessionId),
      })
    );
  });

  test('disables input while loading', async () => {
    fetch.mockImplementation(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                json: async () => ({
                  answer: 'Test',
                  sources: [],
                  latency_ms: 0,
                }),
              }),
            100
          )
        )
    );

    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    const button = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.click(button);

    expect(input).toBeDisabled();
    expect(button).toBeDisabled();

    await waitFor(() => {
      expect(input).not.toBeDisabled();
    });
  });

  test('displays latency when provided', async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({
        answer: 'Test answer',
        sources: [],
        latency_ms: 250,
      }),
    });

    render(<ChatBot />);
    const input = screen.getByPlaceholderText('Ask about the textbook...');
    fireEvent.change(input, { target: { value: 'Test' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    await waitFor(() => {
      expect(screen.getByText('Answered in 250ms')).toBeInTheDocument();
    });
  });
});
