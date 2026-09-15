import React, { useState } from 'react';
import { Bot, User, Quote, FileEdit, Sparkles, Copy, Check, Layout } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChatMessage, Citation } from '../types';

interface MessageBubbleProps {
  message: ChatMessage;
  onCitationClick: (citation: Citation) => void;
  onGenerateShip30: (content: string) => void;
  onGenerateArtifact: (content: string) => void;
  onOpenArtifact?: () => void;
  hasArtifact?: boolean;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  onCitationClick,
  onGenerateShip30,
  onGenerateArtifact,
  onOpenArtifact,
  hasArtifact,
}) => {
  const [copied, setCopied] = useState(false);
  const isUser = message.role === 'user';

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-6 group`}>
      <div className={`flex max-w-3xl space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
          isUser ? 'bg-surface-800 text-surface-200' : 'bg-lenny-600 text-white shadow-md shadow-lenny-600/30'
        }`}>
          {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
        </div>

        {/* Bubble Content */}
        <div className="flex flex-col space-y-2 max-w-2xl">
          <div className={`p-4 rounded-2xl ${
            isUser 
              ? 'bg-surface-800 text-surface-50 rounded-tr-xs' 
              : 'bg-surface-900 border border-surface-800 text-surface-100 rounded-tl-xs shadow-xs'
          }`}>
            <div className="prose prose-invert prose-indigo text-sm leading-relaxed max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>

            {/* Citations Footer */}
            {message.citations && message.citations.length > 0 && (
              <div className="mt-4 pt-3 border-t border-surface-800 flex flex-wrap items-center gap-1.5">
                <span className="text-[11px] font-semibold text-surface-400 uppercase tracking-wider mr-1 flex items-center">
                  <Quote className="w-3 h-3 mr-1 text-lenny-400" />
                  Sources:
                </span>
                {message.citations.map((c, idx) => (
                  <button
                    key={c.id || idx}
                    onClick={() => onCitationClick(c)}
                    className="inline-flex items-center space-x-1 px-2.5 py-1 bg-surface-950 hover:bg-lenny-500/20 border border-surface-800 hover:border-lenny-500/40 rounded-full text-xs text-surface-300 hover:text-lenny-200 transition-colors shadow-2xs"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-lenny-400" />
                    <span className="font-medium truncate max-w-[140px]">{c.guest}</span>
                    {c.timestamp && <span className="text-[10px] text-surface-400 font-mono">[{c.timestamp}]</span>}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Action Toolbar for Assistant Messages */}
          {!isUser && (
            <div className="flex items-center space-x-2 text-xs text-surface-400 px-1 opacity-80 group-hover:opacity-100 transition-opacity">
              <button
                onClick={handleCopy}
                className="inline-flex items-center space-x-1 hover:text-surface-200 transition-colors"
                title="Copy response"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>

              <span className="text-surface-800">•</span>

              <button
                onClick={() => onGenerateShip30(message.content)}
                className="inline-flex items-center space-x-1 hover:text-lenny-300 transition-colors"
                title="Transform this insight into a ~1,250-word Ship 30 for 30 essay"
              >
                <FileEdit className="w-3.5 h-3.5 text-lenny-400" />
                <span>Draft Ship 30 Essay</span>
              </button>

              <span className="text-surface-800">•</span>

              <button
                onClick={() => onGenerateArtifact(message.content)}
                className="inline-flex items-center space-x-1 hover:text-indigo-300 transition-colors"
                title="Create an interactive visual tool or matrix"
              >
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                <span>Make Artifact</span>
              </button>

              {hasArtifact && onOpenArtifact && (
                <>
                  <span className="text-surface-800">•</span>
                  <button
                    onClick={onOpenArtifact}
                    className="inline-flex items-center space-x-1 text-lenny-400 hover:text-lenny-300 font-semibold"
                  >
                    <Layout className="w-3.5 h-3.5" />
                    <span>View Artifact</span>
                  </button>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
