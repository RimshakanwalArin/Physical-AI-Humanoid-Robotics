import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import SelectTextHandler from './SelectTextHandler';

describe('SelectTextHandler Component', () => {
  test('renders without error', () => {
    render(<SelectTextHandler />);
    // Component should render, initially with no button
    const container = document.querySelector('.ask-ai-button');
    expect(container).not.toBeInTheDocument();
  });

  test('shows button on text selection', () => {
    render(
      <div>
        <SelectTextHandler />
        <p>This is selectable text for testing purposes</p>
      </div>
    );

    // Select text
    const paragraph = screen.getByText('This is selectable text for testing purposes');
    const selection = window.getSelection();

    // Mock selection
    const range = document.createRange();
    range.selectNodeContents(paragraph);
    selection.addRange(range);

    // Trigger mouseup event
    fireEvent.mouseUp(document);

    // Button should appear
    const button = screen.getByRole('button', { name: 'Ask AI' });
    expect(button).toBeInTheDocument();
  });

  test('hides button when no text is selected', () => {
    render(
      <div>
        <SelectTextHandler />
        <p>Some text</p>
      </div>
    );

    // Trigger mouseup with no selection
    const selection = window.getSelection();
    selection.removeAllRanges();
    fireEvent.mouseUp(document);

    // Button should not appear
    const button = document.querySelector('.ask-ai-button');
    expect(button).not.toBeInTheDocument();
  });

  test('dispatches custom event on button click', () => {
    const customEventListener = jest.fn();
    document.addEventListener('ask-ai', customEventListener);

    render(
      <div>
        <SelectTextHandler />
        <p>Test text to select</p>
      </div>
    );

    // Select text
    const paragraph = screen.getByText('Test text to select');
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(paragraph);
    selection.addRange(range);

    // Trigger selection
    fireEvent.mouseUp(document);

    // Click button
    const button = screen.getByRole('button', { name: 'Ask AI' });
    fireEvent.click(button);

    // Check if custom event was dispatched
    expect(customEventListener).toHaveBeenCalled();
    const event = customEventListener.mock.calls[0][0];
    expect(event.detail.text).toBe('Test text to select');

    // Cleanup
    document.removeEventListener('ask-ai', customEventListener);
  });

  test('button position follows selection', () => {
    render(
      <div>
        <SelectTextHandler />
        <p style={{ marginTop: '200px' }}>Positioned text</p>
      </div>
    );

    const paragraph = screen.getByText('Positioned text');
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(paragraph);
    selection.addRange(range);

    fireEvent.mouseUp(document);

    const button = screen.getByRole('button', { name: 'Ask AI' });
    const style = button.getAttribute('style');

    // Button should have position styles
    expect(style).toContain('position');
    expect(style).toContain('top');
    expect(style).toContain('left');
  });

  test('handles empty selection correctly', () => {
    render(
      <div>
        <SelectTextHandler />
        <p>Text</p>
      </div>
    );

    // Select and then deselect
    const paragraph = screen.getByText('Text');
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(paragraph);
    selection.addRange(range);

    fireEvent.mouseUp(document);

    // Verify button appeared
    expect(screen.getByRole('button', { name: 'Ask AI' })).toBeInTheDocument();

    // Clear selection
    selection.removeAllRanges();
    fireEvent.mouseUp(document);

    // Button should disappear
    expect(screen.queryByRole('button', { name: 'Ask AI' })).not.toBeInTheDocument();
  });

  test('cleans up event listener on unmount', () => {
    const { unmount } = render(<SelectTextHandler />);

    const spy = jest.spyOn(document, 'removeEventListener');
    unmount();

    expect(spy).toHaveBeenCalledWith('mouseup', expect.any(Function));
    spy.mockRestore();
  });
});
