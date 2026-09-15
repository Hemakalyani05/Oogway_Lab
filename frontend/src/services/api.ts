import { SessionSummary, SessionDetail, ModelInfo, Artifact, StreamEvent } from '../types';

const API_BASE = '/api/v1';

export async function fetchSessions(userId: string = 'default_user'): Promise<SessionSummary[]> {
  const res = await fetch(`${API_BASE}/sessions?user_id=${encodeURIComponent(userId)}`);
  if (!res.ok) throw new Error('Failed to load sessions');
  return res.json();
}

export async function createSession(title: string = 'New Conversation', activeModel: string = 'mock'): Promise<SessionDetail> {
  const res = await fetch(`${API_BASE}/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, active_model: activeModel, user_id: 'default_user' }),
  });
  if (!res.ok) throw new Error('Failed to create session');
  return res.json();
}

export async function fetchSessionDetail(sessionId: string): Promise<SessionDetail> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`);
  if (!res.ok) throw new Error('Failed to load session');
  return res.json();
}

export async function deleteSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete session');
}

export async function fetchModels(): Promise<ModelInfo[]> {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error('Failed to load models');
  return res.json();
}

export async function fetchSessionArtifacts(sessionId: string): Promise<Artifact[]> {
  const res = await fetch(`${API_BASE}/artifacts/session/${sessionId}`);
  if (!res.ok) return [];
  return res.json();
}

export async function streamChat(
  message: string,
  sessionId?: string,
  provider?: string,
  generateShip30: boolean = false,
  generateArtifact: boolean = false,
  onEvent?: (event: StreamEvent) => void,
  signal?: AbortSignal
): Promise<void> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      provider,
      generate_ship30: generateShip30,
      generate_artifact: generateArtifact,
    }),
    signal,
  });

  if (!res.ok) {
    throw new Error(`Chat API error: ${res.status}`);
  }

  const reader = res.body?.getReader();
  if (!reader) return;

  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n\n');
    buffer = lines.pop() || '';

    for (const block of lines) {
      const line = block.trim();
      if (line.startsWith('data: ')) {
        const jsonStr = line.slice(6);
        try {
          const event: StreamEvent = JSON.parse(jsonStr);
          onEvent?.(event);
        } catch (e) {
          console.error('SSE JSON parse error:', e, jsonStr);
        }
      }
    }
  }
}
