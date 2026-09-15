import React from 'react';
import { 
  Plus, 
  MessageSquare, 
  Trash2, 
  Database, 
  Radio, 
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import { SessionSummary } from '../types';

interface SidebarProps {
  sessions: SessionSummary[];
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
  onNewChat: () => void;
  onDeleteSession: (id: string, e: React.MouseEvent) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) => {
  return (
    <aside className="w-64 h-full bg-surface-900 border-r border-surface-800 flex flex-col shrink-0 select-none">
      {/* App Header */}
      <div className="p-4 border-b border-surface-800 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-lenny-600 flex items-center justify-center text-white font-bold shadow-md shadow-lenny-600/30">
            L
          </div>
          <div>
            <h1 className="font-bold text-sm text-surface-100 tracking-tight leading-none">
              Lenny Assistant
            </h1>
            <span className="text-[10px] text-surface-400 font-mono">Growth & PM AI</span>
          </div>
        </div>
      </div>

      {/* New Chat CTA */}
      <div className="p-3">
        <button
          onClick={onNewChat}
          className="w-full py-2 px-3 bg-lenny-600 hover:bg-lenny-500 text-white rounded-lg text-xs font-semibold flex items-center justify-center space-x-2 transition-all shadow-md shadow-lenny-600/20 active:scale-[0.98]"
        >
          <Plus className="w-4 h-4" />
          <span>New Conversation</span>
        </button>
      </div>

      {/* Session List */}
      <div className="flex-1 overflow-y-auto px-2 space-y-0.5">
        <div className="px-2 py-1.5 text-[10px] uppercase font-bold tracking-wider text-surface-500">
          Recent Conversations
        </div>

        {sessions.length === 0 ? (
          <div className="px-3 py-6 text-center text-xs text-surface-500">
            No past conversations
          </div>
        ) : (
          sessions.map((s) => {
            const isActive = s.id === activeSessionId;
            return (
              <div
                key={s.id}
                onClick={() => onSelectSession(s.id)}
                className={`group flex items-center justify-between px-3 py-2 rounded-lg text-xs cursor-pointer transition-colors ${
                  isActive 
                    ? 'bg-surface-800 text-surface-50 font-medium' 
                    : 'text-surface-400 hover:bg-surface-800/50 hover:text-surface-200'
                }`}
              >
                <div className="flex items-center space-x-2 truncate mr-2">
                  <MessageSquare className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-lenny-400' : 'text-surface-500'}`} />
                  <span className="truncate">{s.title || 'Untitled Chat'}</span>
                </div>
                <button
                  onClick={(e) => onDeleteSession(s.id, e)}
                  title="Delete chat"
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-400 text-surface-500 rounded transition-opacity"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            );
          })
        )}
      </div>

      {/* Knowledge Base Status Footer */}
      <div className="p-3 border-t border-surface-800/80 bg-surface-950/40">
        <div className="flex items-center justify-between text-[11px] text-surface-400 mb-2">
          <div className="flex items-center space-x-1.5">
            <Radio className="w-3 h-3 text-emerald-400 animate-pulse" />
            <span className="text-surface-300 font-medium">Knowledge Base</span>
          </div>
          <span className="font-mono text-[10px] bg-surface-800 px-1.5 py-0.5 rounded text-surface-300">
            9 Episodes
          </span>
        </div>
        <p className="text-[10px] text-surface-400 leading-tight">
          Chesky, Verna, Doshi, Rajaram, Vo, Winters, Alströmer, Ellis, Rachitsky.
        </p>
      </div>
    </aside>
  );
};
