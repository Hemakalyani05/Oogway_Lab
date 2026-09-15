import React, { useRef, useEffect } from 'react';
import { Send, Square, Sparkles, FileEdit, ArrowUp } from 'lucide-react';
import { ChatMessage, Citation } from '../types';
import { MessageBubble } from './MessageBubble';
import { QuickPrompts } from './QuickPrompts';

interface ChatAreaProps {
  messages: ChatMessage[];
  streamingToken: string;
  streamingStatus: string;
  streamingCitations: Citation[];
  isStreaming: boolean;
  onSendMessage: (msg: string, generateShip30?: boolean, generateArtifact?: boolean) => void;
  onStopStreaming: () => void;
  onCitationClick: (citation: Citation) => void;
  onOpenArtifact?: () => void;
  hasActiveArtifact?: boolean;
}

export const ChatArea: React.FC<ChatAreaProps> = ({
  messages,
  streamingToken,
  streamingStatus,
  streamingCitations,
  isStreaming,
  onSendMessage,
  onStopStreaming,
  onCitationClick,
  onOpenArtifact,
  hasActiveArtifact,
}) => {
  const [input, setInput] = React.useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingToken, streamingStatus]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (!input.trim() || isStreaming) return;
    onSendMessage(input.trim());
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleTextareaInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 180)}px`;
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-surface-950 relative overflow-hidden">
      {/* Scrollable Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 sm:px-8 py-6">
        {messages.length === 0 && !isStreaming ? (
          <QuickPrompts onSelectPrompt={(prompt, ship30, artifact) => onSendMessage(prompt, ship30, artifact)} />
        ) : (
          <div className="max-w-3xl mx-auto">
            {messages.map((m, idx) => (
              <MessageBubble
                key={idx}
                message={m}
                onCitationClick={onCitationClick}
                onGenerateShip30={(content) => onSendMessage(`Please draft a ~1,250-word Ship 30 for 30 essay based on this: ${content}`, true, false)}
                onGenerateArtifact={(content) => onSendMessage(`Please generate an interactive HTML/CSS tool or calculator artifact based on this: ${content}`, false, true)}
                onOpenArtifact={onOpenArtifact}
                hasArtifact={hasActiveArtifact && idx === messages.length - 1}
              />
            ))}

            {/* Live Streaming Response Bubble */}
            {isStreaming && (
              <div className="flex w-full justify-start mb-6">
                <div className="flex max-w-3xl space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-lenny-600 flex items-center justify-center text-white shrink-0 shadow-md shadow-lenny-600/30">
                    <Sparkles className="w-4 h-4 animate-spin" />
                  </div>
                  <div className="flex flex-col space-y-2 max-w-2xl">
                    <div className="p-4 rounded-2xl bg-surface-900 border border-surface-800 text-surface-100 rounded-tl-xs shadow-xs">
                      {streamingStatus && !streamingToken && (
                        <div className="flex items-center space-x-2 text-xs text-lenny-400 py-1">
                          <span className="w-2 h-2 rounded-full bg-lenny-400 animate-ping" />
                          <span>{streamingStatus}</span>
                        </div>
                      )}

                      {streamingToken && (
                        <div className="prose prose-invert prose-indigo text-sm leading-relaxed whitespace-pre-wrap">
                          {streamingToken}
                          <span className="inline-block w-1.5 h-4 ml-1 bg-lenny-400 animate-pulse align-middle" />
                        </div>
                      )}

                      {streamingCitations.length > 0 && (
                        <div className="mt-3 pt-2 border-t border-surface-800 flex flex-wrap gap-1.5">
                          {streamingCitations.map((c, i) => (
                            <span key={i} className="text-[10px] px-2 py-0.5 bg-surface-950 text-surface-400 rounded-full border border-surface-800">
                              {c.guest} [{c.timestamp}]
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Bar */}
      <div className="p-4 border-t border-surface-800/80 bg-surface-950/80 backdrop-blur-md">
        <div className="max-w-3xl mx-auto relative">
          <div className="flex items-end bg-surface-900 border border-surface-800 focus-within:border-lenny-500 rounded-2xl p-2 shadow-lg transition-colors">
            <textarea
              ref={textareaRef}
              rows={1}
              value={input}
              onChange={handleTextareaInput}
              onKeyDown={handleKeyDown}
              placeholder="Ask a PM or growth question from Lenny's transcripts..."
              className="flex-1 bg-transparent border-0 resize-none text-sm text-surface-100 placeholder-surface-500 focus:outline-none focus:ring-0 px-3 py-1.5 max-h-44"
            />

            <div className="flex items-center space-x-1 pl-2">
              {isStreaming ? (
                <button
                  onClick={onStopStreaming}
                  className="p-2 bg-red-500/20 text-red-400 hover:bg-red-500/30 rounded-xl transition-colors"
                  title="Stop generating"
                >
                  <Square className="w-4 h-4" />
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  disabled={!input.trim()}
                  className={`p-2 rounded-xl transition-all ${
                    input.trim() 
                      ? 'bg-lenny-600 hover:bg-lenny-500 text-white shadow-md shadow-lenny-600/30 active:scale-95' 
                      : 'bg-surface-800 text-surface-500 cursor-not-allowed'
                  }`}
                  title="Send message"
                >
                  <ArrowUp className="w-4 h-4 stroke-[2.5]" />
                </button>
              )}
            </div>
          </div>
          <div className="flex items-center justify-between text-[11px] text-surface-400 mt-2 px-2">
            <span>Press <kbd className="px-1 py-0.5 bg-surface-900 border border-surface-800 rounded text-[10px] text-surface-400">Enter</kbd> to send, <kbd className="px-1 py-0.5 bg-surface-900 border border-surface-800 rounded text-[10px] text-surface-400">Shift+Enter</kbd> for newline</span>
            <span>Grounded RAG Engine</span>
          </div>
        </div>
      </div>
    </div>
  );
};
