import { useState, useCallback, useRef } from 'react';
import { ChatMessage, Citation, Artifact, StreamEvent } from '../types';
import { streamChat } from '../services/api';

export function useChat(activeSessionId: string | null, selectedProvider: string, onSessionCreated?: (id: string) => void) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streamingToken, setStreamingToken] = useState<string>('');
  const [streamingStatus, setStreamingStatus] = useState<string>('');
  const [streamingCitations, setStreamingCitations] = useState<Citation[]>([]);
  const [activeArtifact, setActiveArtifact] = useState<Artifact | null>(null);
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (text: string, generateShip30: boolean = false, generateArtifact: boolean = false) => {
      if (!text.trim() || isStreaming) return;

      const userMsg: ChatMessage = {
        role: 'user',
        content: text,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setIsStreaming(true);
      setStreamingToken('');
      setStreamingStatus('Connecting...');
      setStreamingCitations([]);

      abortControllerRef.current = new AbortController();

      let accumulatedText = '';
      let accumulatedCitations: Citation[] = [];
      let detectedArtifact: Artifact | null = null;
      let currentSessionId = activeSessionId;

      try {
        await streamChat(
          text,
          activeSessionId || undefined,
          selectedProvider,
          generateShip30,
          generateArtifact,
          (event: StreamEvent) => {
            if (event.type === 'session_init' && event.session_id) {
              currentSessionId = event.session_id;
              if (!activeSessionId && onSessionCreated) {
                onSessionCreated(event.session_id);
              }
            } else if (event.type === 'status' && event.message) {
              setStreamingStatus(event.message);
            } else if (event.type === 'citations' && event.citations) {
              accumulatedCitations = event.citations;
              setStreamingCitations(event.citations);
            } else if (event.type === 'token' && event.token) {
              accumulatedText += event.token;
              setStreamingToken(accumulatedText);
            } else if (event.type === 'artifact' && event.artifact) {
              detectedArtifact = event.artifact;
              setActiveArtifact(event.artifact);
            } else if (event.type === 'done') {
              const cleanContent = event.full_content || accumulatedText;
              const assistantMsg: ChatMessage = {
                role: 'assistant',
                content: cleanContent,
                citations: accumulatedCitations,
                created_at: new Date().toISOString(),
              };
              setMessages((prev) => [...prev, assistantMsg]);
              if (event.artifact) {
                setActiveArtifact(event.artifact);
              }
            }
          },
          abortControllerRef.current.signal
        );
      } catch (err: any) {
        if (err.name !== 'AbortError') {
          console.error('Streaming failed:', err);
          const errorMsg: ChatMessage = {
            role: 'assistant',
            content: `**Error:** Failed to stream response. (${err.message || 'Network error'})`,
            created_at: new Date().toISOString(),
          };
          setMessages((prev) => [...prev, errorMsg]);
        }
      } finally {
        setIsStreaming(false);
        setStreamingToken('');
        setStreamingStatus('');
        abortControllerRef.current = null;
      }
    },
    [activeSessionId, isStreaming, selectedProvider, onSessionCreated]
  );

  const stopStreaming = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsStreaming(false);
      setStreamingToken('');
      setStreamingStatus('');
    }
  }, []);

  return {
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
  };
}
