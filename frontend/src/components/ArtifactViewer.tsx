import React, { useEffect, useState } from 'react';
import {
  X,
  Copy,
  Check,
  Download,
  Code2,
  Eye,
  FileText,
  Smartphone,
  Tablet,
  Monitor,
  Maximize2,
  Minimize2
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Artifact } from '../types';
import { SandboxedIframe } from './SandboxedIframe';

interface ArtifactViewerProps {
  artifact: Artifact | null;
  onClose: () => void;
}

export const ArtifactViewer: React.FC<ArtifactViewerProps> = ({
  artifact,
  onClose
}) => {
  const [tab, setTab] = useState<'preview' | 'code' | 'markdown'>('preview');
  const [viewport, setViewport] = useState<'desktop' | 'tablet' | 'mobile'>(
    'desktop'
  );
  const [copied, setCopied] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Always open a newly selected artifact in Preview mode.
  useEffect(() => {
    if (artifact) {
      setTab(artifact.artifact_type === 'html' ? 'preview' : 'markdown');
      setIsFullscreen(false);
    }
  }, [artifact]);

  if (!artifact) return null;

  const isHtml = artifact.artifact_type === 'html';

  const handleCopy = async () => {
    await navigator.clipboard.writeText(artifact.content);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);
  };

  const handleDownload = () => {
    const ext = isHtml ? 'html' : 'md';

    const blob = new Blob([artifact.content], {
      type: isHtml ? 'text/html' : 'text/markdown'
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');

    a.href = url;
    a.download = `${artifact.title.replace(/\s+/g, '_')}.${ext}`;

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
  };

  const getViewportWidth = () => {
    if (viewport === 'mobile') return 'max-w-sm';
    if (viewport === 'tablet') return 'max-w-xl';
    return 'w-full';
  };

  return (
    <div
      className={`h-full flex flex-col bg-surface-900 border-l border-surface-800 transition-all duration-300 ${
        isFullscreen
          ? 'fixed inset-0 z-50 bg-surface-950'
          : 'w-full'
      }`}
    >
      {/* Header */}
      <div className="h-14 px-4 border-b border-surface-800 flex items-center justify-between bg-surface-900/90 backdrop-blur-xs">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="p-1.5 bg-lenny-500/20 text-lenny-400 rounded-md">
            {isHtml ? (
              <Code2 className="w-4 h-4" />
            ) : (
              <FileText className="w-4 h-4" />
            )}
          </div>

          <div className="truncate">
            <h3 className="text-sm font-semibold text-surface-100 truncate">
              {artifact.title}
            </h3>

            <span className="text-xs text-surface-400 uppercase tracking-wider font-mono">
              {artifact.artifact_type} • {artifact.language}
            </span>
          </div>
        </div>

        {/* Controls */}
        <div className="flex items-center space-x-1">

          {/* Tabs */}
          <div className="flex bg-surface-950 p-0.5 rounded-lg border border-surface-800 mr-2">
            {isHtml && (
              <button
                onClick={() => setTab('preview')}
                className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors flex items-center space-x-1 ${
                  tab === 'preview'
                    ? 'bg-surface-800 text-surface-50 shadow-xs'
                    : 'text-surface-400 hover:text-surface-200'
                }`}
              >
                <Eye className="w-3 h-3" />
                <span>Preview</span>
              </button>
            )}

            <button
              onClick={() =>
                setTab(isHtml ? 'code' : 'markdown')
              }
              className={`px-2.5 py-1 text-xs font-medium rounded-md transition-colors flex items-center space-x-1 ${
                (isHtml && tab === 'code') ||
                (!isHtml && tab === 'markdown')
                  ? 'bg-surface-800 text-surface-50 shadow-xs'
                  : 'text-surface-400 hover:text-surface-200'
              }`}
            >
              <Code2 className="w-3 h-3" />
              <span>{isHtml ? 'Code' : 'Document'}</span>
            </button>
          </div>

          {/* Viewport controls */}
          {isHtml && tab === 'preview' && (
            <div className="hidden sm:flex bg-surface-950 p-0.5 rounded-lg border border-surface-800 mr-2">
              <button
                onClick={() => setViewport('desktop')}
                title="Desktop View"
                className={`p-1 rounded-md ${
                  viewport === 'desktop'
                    ? 'bg-surface-800 text-lenny-400'
                    : 'text-surface-400 hover:text-surface-200'
                }`}
              >
                <Monitor className="w-3.5 h-3.5" />
              </button>

              <button
                onClick={() => setViewport('tablet')}
                title="Tablet View"
                className={`p-1 rounded-md ${
                  viewport === 'tablet'
                    ? 'bg-surface-800 text-lenny-400'
                    : 'text-surface-400 hover:text-surface-200'
                }`}
              >
                <Tablet className="w-3.5 h-3.5" />
              </button>

              <button
                onClick={() => setViewport('mobile')}
                title="Mobile View"
                className={`p-1 rounded-md ${
                  viewport === 'mobile'
                    ? 'bg-surface-800 text-lenny-400'
                    : 'text-surface-400 hover:text-surface-200'
                }`}
              >
                <Smartphone className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Copy */}
          <button
            onClick={handleCopy}
            title="Copy Content"
            className="p-1.5 text-surface-400 hover:text-surface-100 hover:bg-surface-800 rounded-md transition-colors"
          >
            {copied ? (
              <Check className="w-4 h-4 text-emerald-400" />
            ) : (
              <Copy className="w-4 h-4" />
            )}
          </button>

          {/* Download */}
          <button
            onClick={handleDownload}
            title="Download File"
            className="p-1.5 text-surface-400 hover:text-surface-100 hover:bg-surface-800 rounded-md transition-colors"
          >
            <Download className="w-4 h-4" />
          </button>

          {/* Fullscreen */}
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
            className="p-1.5 text-surface-400 hover:text-surface-100 hover:bg-surface-800 rounded-md transition-colors"
          >
            {isFullscreen ? (
              <Minimize2 className="w-4 h-4" />
            ) : (
              <Maximize2 className="w-4 h-4" />
            )}
          </button>

          {/* Close */}
          <button
            onClick={onClose}
            title="Close Artifact Pane"
            className="p-1.5 text-surface-400 hover:text-surface-100 hover:bg-surface-800 rounded-md transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4 flex justify-center bg-surface-950/50">

        {/* HTML Preview */}
        {isHtml && tab === 'preview' ? (
          <div className="w-full h-full flex justify-center transition-all duration-200">
            <div
              className={`${getViewportWidth()} h-full shadow-2xl`}
            >
              <SandboxedIframe
                content={artifact.content}
                title={artifact.title}
              />
            </div>
          </div>

        ) : isHtml && tab === 'code' ? (

          /* HTML Code */
          <div className="w-full h-full bg-surface-950 p-4 rounded-lg border border-surface-800 overflow-auto font-mono text-xs text-surface-200 leading-relaxed">
            <pre className="whitespace-pre-wrap">
              {artifact.content}
            </pre>
          </div>

        ) : (

          /* Markdown */
          <div className="w-full max-w-3xl bg-surface-900 p-8 rounded-xl border border-surface-800 shadow-xl overflow-auto prose prose-invert prose-indigo max-w-none text-surface-100">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {artifact.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
};