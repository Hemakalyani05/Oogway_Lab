export interface Citation {
  id: string;
  episode_title: string;
  guest: string;
  timestamp?: string;
  quote: string;
  relevance_score?: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  citations?: Citation[];
  created_at?: string;
}

export interface SessionSummary {
  id: string;
  title: string;
  user_id: string;
  active_model: string;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface SessionDetail {
  id: string;
  title: string;
  user_id: string;
  active_model: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface Artifact {
  id?: string;
  session_id?: string;
  title: string;
  artifact_type: 'html' | 'markdown' | 'css' | 'javascript';
  language: string;
  content: string;
  metadata_json?: Record<string, any>;
  created_at?: string;
}

export interface ModelInfo {
  provider_id: string;
  display_name: string;
  model_name: string;
  is_available: boolean;
  is_local: boolean;
  description: string;
  recommended: boolean;
}

export interface StreamEvent {
  type: 'status' | 'citations' | 'token' | 'artifact' | 'done' | 'error' | 'session_init';
  message?: string;
  token?: string;
  citations?: Citation[];
  artifact?: Artifact;
  full_content?: string;
  raw_content?: string;
  session_id?: string;
  model_used?: string;
}
