import { useState, useEffect, useCallback } from 'react';
import { SessionSummary, SessionDetail } from '../types';
import { fetchSessions, createSession, deleteSession, fetchSessionDetail } from '../services/api';

export function useSessions() {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadSessions = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetchSessions();
      setSessions(data);
      if (data.length > 0 && !activeSessionId) {
        // Optionally select first
      }
    } catch (err) {
      console.error('Failed to fetch sessions:', err);
    } finally {
      setLoading(false);
    }
  }, [activeSessionId]);

  useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  const handleNewChat = useCallback(async () => {
    try {
      const newSess = await createSession('New Conversation');
      setSessions((prev) => [
        {
          id: newSess.id,
          title: newSess.title,
          user_id: newSess.user_id,
          active_model: newSess.active_model,
          message_count: 0,
          created_at: newSess.created_at,
          updated_at: newSess.updated_at,
        },
        ...prev,
      ]);
      setActiveSessionId(newSess.id);
      return newSess.id;
    } catch (err) {
      console.error('Failed to create new session:', err);
      return null;
    }
  }, []);

  const handleDeleteSession = useCallback(async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await deleteSession(id);
      setSessions((prev) => prev.filter((s) => s.id !== id));
      if (activeSessionId === id) {
        setActiveSessionId(null);
      }
    } catch (err) {
      console.error('Failed to delete session:', err);
    }
  }, [activeSessionId]);

  return {
    sessions,
    setSessions,
    activeSessionId,
    setActiveSessionId,
    loading,
    loadSessions,
    handleNewChat,
    handleDeleteSession,
  };
}
