import React, { useEffect, useState } from 'react';
import { Cloud, Server } from 'lucide-react';
import { ModelInfo } from '../types';
import { fetchModels } from '../services/api';

interface ModelSelectorProps {
  selectedProvider: string;
  onSelectProvider: (providerId: string, modelName: string) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  selectedProvider,
  onSelectProvider,
}) => {
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModels()
      .then((data) => {
        console.log('MODELS FROM API:', data);
        setModels(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load models:', err);
        setLoading(false);
      });
  }, []);

  const currentModel = models.find(
    (model) => model.provider_id === selectedProvider
  );

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const providerId = event.target.value;
    const model = models.find(
      (item) => item.provider_id === providerId
    );

    if (model) {
      onSelectProvider(model.provider_id, model.model_name);
    }
  };

  return (
    <div className="flex items-center space-x-2">
      {currentModel?.is_local ? (
        <Server className="w-4 h-4 text-emerald-400" />
      ) : (
        <Cloud className="w-4 h-4 text-blue-400" />
      )}

      <select
        value={selectedProvider}
        onChange={handleChange}
        disabled={loading || models.length === 0}
        className="px-3 py-1.5 bg-surface-900 border border-surface-800 rounded-lg text-xs font-medium text-surface-100 outline-none cursor-pointer hover:bg-surface-800 disabled:opacity-50"
      >
        {loading ? (
          <option value="">Loading models...</option>
        ) : (
          models.map((model) => (
            <option
              key={model.provider_id}
              value={model.provider_id}
            >
              {model.display_name}
            </option>
          ))
        )}
      </select>
    </div>
  );
};