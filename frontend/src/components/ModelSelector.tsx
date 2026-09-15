import React, { useState, useEffect } from 'react';
import { Cpu, ChevronDown, Check, Sparkles, Cloud, Server, AlertCircle } from 'lucide-react';
import { ModelInfo } from '../types';
import { fetchModels } from '../services/api';

interface ModelSelectorProps {
  selectedProvider: string;
  onSelectProvider: (providerId: string, modelName: string) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({ selectedProvider, onSelectProvider }) => {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModels()
      .then((data) => {
        setModels(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load models:', err);
        setLoading(false);
      });
  }, []);

  const currentModel = models.find((m) => m.provider_id === selectedProvider) || models[0];

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-1.5 bg-surface-900 hover:bg-surface-800 border border-surface-800 rounded-lg text-xs font-medium text-surface-200 transition-all shadow-xs"
      >
        <div className="flex items-center space-x-1.5">
          <span className={`w-2 h-2 rounded-full ${currentModel?.is_available ? 'bg-emerald-500 shadow-xs shadow-emerald-500/50' : 'bg-amber-500'}`} />
          {currentModel?.is_local ? (
            <Server className="w-3.5 h-3.5 text-indigo-400" />
          ) : (
            <Cloud className="w-3.5 h-3.5 text-sky-400" />
          )}
          <span className="font-semibold text-surface-100">{currentModel?.display_name || 'Select Model'}</span>
        </div>
        <ChevronDown className="w-3.5 h-3.5 text-surface-400" />
      </button>

      {isOpen && (
        <>
          <div className="fixed inset-0 z-30" onClick={() => setIsOpen(false)} />
          <div className="absolute right-0 mt-2 w-72 bg-surface-900 border border-surface-800 rounded-xl shadow-2xl z-40 p-2 space-y-1">
            <div className="px-2 py-1.5 border-b border-surface-800/80 mb-1">
              <span className="text-[10px] uppercase font-bold tracking-wider text-surface-400">
                Model Provider & Engine
              </span>
            </div>

            {models.map((m) => {
              const isSelected = m.provider_id === selectedProvider;
              return (
                <button
                  key={m.provider_id}
                  onClick={() => {
                    onSelectProvider(m.provider_id, m.model_name);
                    setIsOpen(false);
                  }}
                  className={`w-full text-left p-2.5 rounded-lg flex items-start justify-between transition-colors ${
                    isSelected ? 'bg-lenny-500/15 border border-lenny-500/30' : 'hover:bg-surface-800 border border-transparent'
                  }`}
                >
                  <div className="space-y-0.5">
                    <div className="flex items-center space-x-1.5">
                      <span className={`w-1.5 h-1.5 rounded-full ${m.is_available ? 'bg-emerald-500' : 'bg-amber-500'}`} />
                      <span className="text-xs font-semibold text-surface-100">{m.display_name}</span>
                      {m.recommended && (
                        <span className="px-1.5 py-0.5 text-[9px] bg-indigo-500/20 text-indigo-300 rounded font-medium">
                          Local Demo
                        </span>
                      )}
                    </div>
                    <p className="text-[11px] text-surface-400 leading-tight">
                      {m.description}
                    </p>
                  </div>
                  {isSelected && <Check className="w-4 h-4 text-lenny-400 shrink-0 ml-2 mt-0.5" />}
                </button>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};
