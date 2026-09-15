import React from 'react';
import { Sparkles, ArrowRight, Zap, Target, Layers, FileEdit } from 'lucide-react';

interface QuickPromptsProps {
  onSelectPrompt: (prompt: string, generateShip30?: boolean, generateArtifact?: boolean) => void;
}

export const QuickPrompts: React.FC<QuickPromptsProps> = ({ onSelectPrompt }) => {
  const samplePrompts = [
    {
      title: "Founder Mode vs Manager Mode",
      guest: "Brian Chesky (Airbnb)",
      prompt: "Explain Brian Chesky's Founder Mode vs Manager Mode from his YC talk and Lenny's podcast. What did Airbnb replace traditional PM with?",
      icon: <Target className="w-4 h-4 text-indigo-400" />
    },
    {
      title: "B2B Product-Led Growth & PQLs",
      guest: "Elena Verna",
      prompt: "What are the core loops in B2B Product-Led Growth according to Elena Verna? How should growth teams define PQLs and activation milestones?",
      icon: <Zap className="w-4 h-4 text-amber-400" />
    },
    {
      title: "SPADE Decision Matrix Calculator",
      guest: "Gokul Rajaram",
      prompt: "Generate an interactive SPADE Decision Matrix calculator artifact in HTML/CSS based on Gokul Rajaram's framework.",
      icon: <Layers className="w-4 h-4 text-emerald-400" />,
      generateArtifact: true
    },
    {
      title: "Ship 30 Essay: High-Leverage PMs",
      guest: "Shreyas Doshi",
      prompt: "Write a 1,250-word Ship 30 for 30 Atomic Essay on Shreyas Doshi's LNO Framework and how great PMs operate with high agency.",
      icon: <FileEdit className="w-4 h-4 text-purple-400" />,
      generateShip30: true
    }
  ];

  return (
    <div className="w-full max-w-2xl px-4 py-8 mx-auto text-center">
      <div className="inline-flex items-center space-x-2 px-3 py-1 bg-lenny-500/10 border border-lenny-500/20 rounded-full text-xs font-medium text-lenny-300 mb-4">
        <Sparkles className="w-3.5 h-3.5" />
        <span>Grounded strictly in Lenny's Podcast Transcripts</span>
      </div>

      <h2 className="text-2xl sm:text-3xl font-bold text-surface-100 tracking-tight mb-2">
        What product challenge are you solving?
      </h2>
      <p className="text-sm text-surface-400 max-w-md mx-auto mb-8">
        Ask complex product strategy and growth questions, draft Ship 30 essays, or generate live interactive artifacts.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => onSelectPrompt(p.prompt, p.generateShip30, p.generateArtifact)}
            className="p-4 bg-surface-900/80 hover:bg-surface-800 border border-surface-800 hover:border-surface-700 rounded-xl text-left transition-all duration-200 group flex flex-col justify-between shadow-xs hover:shadow-md"
          >
            <div>
              <div className="flex items-center space-x-2 mb-1.5">
                {p.icon}
                <h4 className="text-xs font-semibold text-surface-200 group-hover:text-surface-100 transition-colors">
                  {p.title}
                </h4>
              </div>
              <p className="text-xs text-surface-400 line-clamp-2">
                {p.prompt}
              </p>
            </div>
            <div className="mt-3 pt-2 border-t border-surface-800/60 flex items-center justify-between text-[10px] text-surface-400">
              <span className="font-mono text-lenny-400">{p.guest}</span>
              <ArrowRight className="w-3 h-3 text-surface-400 group-hover:text-surface-100 transition-transform group-hover:translate-x-0.5" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};
