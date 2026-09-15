import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatArea } from './components/ChatArea';
import { ArtifactViewer } from './components/ArtifactViewer';
import { SourceViewer } from './components/SourceViewer';
import { ModelSelector } from './components/ModelSelector';
import { useSessions } from './hooks/useSessions';
import { useChat } from './hooks/useChat';
import { Citation, Artifact } from './types';
import { fetchSessionDetail, fetchSessionArtifacts } from './services/api';

export const App: React.FC = () => {
  const [selectedProvider, setSelectedProvider] = useState<string>('ollama');
  const [selectedModelName, setSelectedModelName] = useState<string>('llama3.2');
  const [activeCitation, setActiveCitation] = useState<Citation | null>(null);
  const [isArtifactOpen, setIsArtifactOpen] = useState<boolean>(false);

  const {
    sessions,
    setSessions,
    activeSessionId,
    setActiveSessionId,
    handleNewChat,
    handleDeleteSession,
  } = useSessions();

  const {
    messages,
    setMessages,
    streamingToken,
    streamingStatus,
    streamingCitations,
    activeArtifact,
    setActiveArtifact,
    isStreaming,
    sendMessage,
    stopStreaming,
  } = useChat(activeSessionId, selectedProvider, (newId) => {
    setActiveSessionId(newId);
  });

  // When active session changes, load messages and artifacts
  useEffect(() => {
    if (activeSessionId) {
      fetchSessionDetail(activeSessionId)
        .then((detail) => {
          setMessages(detail.messages || []);
        })
        .catch((err) => console.error(err));

      fetchSessionArtifacts(activeSessionId)
        .then((artifacts) => {
          if (artifacts.length > 0) {
            setActiveArtifact(artifacts[0]);
          }
        })
        .catch((err) => console.error(err));
    } else {
      setMessages([]);
      setActiveArtifact(null);
    }
  }, [activeSessionId, setMessages, setActiveArtifact]);

  // When activeArtifact updates, open artifact pane automatically
  useEffect(() => {
    if (activeArtifact) {
      setIsArtifactOpen(true);
    }
  }, [activeArtifact]);

  return (
    <div className="flex h-screen w-screen bg-surface-950 text-surface-50 font-sans overflow-hidden">
      {/* Left Sidebar */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={(id) => setActiveSessionId(id)}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
      />

      {/* Center Main Workspace */}
      <div className="flex-1 flex flex-col h-full min-w-0">
        {/* Top Navbar */}
        <header className="h-14 px-6 border-b border-surface-800 flex items-center justify-between bg-surface-950/80 backdrop-blur-md shrink-0">
          <div className="flex items-center space-x-2 text-xs text-surface-400">
            <span className="font-medium text-surface-200">The Lenny Growth Assistant</span>
            <span>/</span>
            <span className="text-surface-400 font-mono text-[11px]">
              {sessions.find((s) => s.id === activeSessionId)?.title || 'New Session'}
            </span>
          </div>

          <div className="flex items-center space-x-3">
            <ModelSelector
              selectedProvider={selectedProvider}
              onSelectProvider={(prov, model) => {
                setSelectedProvider(prov);
                setSelectedModelName(model);
              }}
            />
          </div>
        </header>

        {/* Center & Right Split Pane Area */}
        <div className="flex-1 flex min-h-0 overflow-hidden">
          {/* Main Chat Area */}
          <div className={`h-full transition-all duration-300 flex flex-col ${isArtifactOpen && activeArtifact ? 'w-1/2 hidden md:flex' : 'w-full'}`}>
            <ChatArea
              messages={messages}
              streamingToken={streamingToken}
              streamingStatus={streamingStatus}
              streamingCitations={streamingCitations}
              isStreaming={isStreaming}
              onSendMessage={sendMessage}
              onStopStreaming={stopStreaming}
              onCitationClick={(cit) => setActiveCitation(cit)}
              onOpenArtifact={() => setIsArtifactOpen(true)}
              hasActiveArtifact={Boolean(activeArtifact)}
            />
          </div>

          {/* Right Artifact Split-Screen Viewer */}
          {isArtifactOpen && activeArtifact && (
            <div className="h-full flex-1 min-w-0 border-l border-surface-800 bg-surface-900 animate-in slide-in-from-right duration-200">
              <ArtifactViewer
                artifact={activeArtifact}
                onClose={() => setIsArtifactOpen(false)}
              />
            </div>
          )}
        </div>
      </div>

      {/* Source Excerpt Drawer Modal */}
      <SourceViewer
        citation={activeCitation}
        onClose={() => setActiveCitation(null)}
      />
    </div>
  );
};
