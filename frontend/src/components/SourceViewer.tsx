import React from 'react';
import { X, ExternalLink, User, Clock, Quote } from 'lucide-react';
import { Citation } from '../types';

interface SourceViewerProps {
  citation: Citation | null;
  onClose: () => void;
}

export const SourceViewer: React.FC<SourceViewerProps> = ({ citation, onClose }) => {
  if (!citation) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-end bg-black/60 backdrop-blur-xs transition-opacity animate-in fade-in duration-200">
      <div 
        className="w-full max-w-md h-full bg-surface-900 border-l border-surface-800 p-6 flex flex-col shadow-2xl overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between pb-4 border-b border-surface-800">
          <div className="flex items-center space-x-2">
            <Quote className="w-5 h-5 text-lenny-400" />
            <h3 className="font-semibold text-surface-100 text-sm">Transcript Source</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-md text-surface-400 hover:text-surface-100 hover:bg-surface-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="mt-5 space-y-4">
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-lenny-400">Episode</span>
            <h4 className="text-base font-medium text-surface-100 mt-1 leading-snug">
              {citation.episode_title}
            </h4>
          </div>

          <div className="flex items-center space-x-4 text-xs text-surface-400 bg-surface-950/60 p-3 rounded-lg border border-surface-800">
            <div className="flex items-center space-x-1.5">
              <User className="w-3.5 h-3.5 text-lenny-400" />
              <span className="font-medium text-surface-200">{citation.guest}</span>
            </div>
            {citation.timestamp && (
              <div className="flex items-center space-x-1.5">
                <Clock className="w-3.5 h-3.5 text-surface-400" />
                <span>{citation.timestamp}</span>
              </div>
            )}
            {citation.relevance_score && (
              <div className="ml-auto text-lenny-400 font-mono">
                Match: {(citation.relevance_score * 100).toFixed(0)}%
              </div>
            )}
          </div>

          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-surface-400">Verified Quote / Excerpt</span>
            <div className="mt-2 p-4 bg-surface-950 rounded-lg border border-surface-800 text-sm text-surface-200 leading-relaxed font-sans whitespace-pre-wrap">
              "{citation.quote}"
            </div>
          </div>

          <div className="pt-4">
            <a
              href="https://www.lennysnewsletter.com/podcast"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 text-xs text-lenny-400 hover:text-lenny-300 transition-colors"
            >
              <span>View full podcast catalog on Lenny's Newsletter</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
