'use client';

import { useState, useTransition, useMemo } from 'react';
import { X, Plus } from 'lucide-react';
import { updateRecipeTags } from './actions';

interface RecipeTagsEditorProps {
  filePath: string;
  initialTags?: string[];
  suggestions?: string[];
}

export default function RecipeTagsEditor({ filePath, initialTags = [], suggestions = [] }: RecipeTagsEditorProps) {
  const [tags, setTags] = useState<string[]>(initialTags);
  const [newTag, setNewTag] = useState('');
  const [isPending, startTransition] = useTransition();

  const sortedTags = useMemo(() => [...tags].sort((a, b) => a.localeCompare(b)), [tags]);
  const filteredSuggestions = useMemo(() => {
    const term = newTag.trim().toLowerCase();
    return suggestions
      .filter((tag) => !tags.includes(tag))
      .filter((tag) => !term || tag.toLowerCase().includes(term))
      .slice(0, 8);
  }, [suggestions, tags, newTag]);

  const addTag = (tag: string) => {
    const value = tag.trim();
    if (!value) return;
    if (tags.includes(value)) {
      setNewTag('');
      return;
    }
    const next = [...tags, value];
    setTags(next);
    setNewTag('');
    persist(next);
  };

  const removeTag = (tag: string) => {
    const next = tags.filter((t) => t !== tag);
    setTags(next);
    persist(next);
  };

  const persist = (next: string[]) => {
    startTransition(async () => {
      const res = await updateRecipeTags(filePath, next);
      if (!res.success) {
        // Roll back on failure
        setTags(tags);
      }
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    addTag(newTag);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 flex-wrap">
        {sortedTags.length === 0 && <span className="text-sm text-neutral-500">No tags yet</span>}
        {sortedTags.map((tag) => (
          <button
            key={tag}
            onClick={() => removeTag(tag)}
            disabled={isPending}
            className="flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-200 text-xs border border-emerald-500/20 hover:border-emerald-400/40 transition-colors disabled:opacity-60"
            title="Click to remove tag"
          >
            {tag}
            <X className="w-3 h-3" />
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <input
          value={newTag}
          onChange={(e) => setNewTag(e.target.value)}
          placeholder="Add tag..."
          className="flex-1 bg-neutral-900/60 border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500/50 transition-colors"
          aria-label="Add tag"
          disabled={isPending}
        />
        <button
          type="submit"
          disabled={isPending}
          className="inline-flex items-center gap-1 px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition-colors disabled:opacity-60"
        >
          <Plus className="w-4 h-4" />
          Add
        </button>
      </form>

      {filteredSuggestions.length > 0 && (
        <div className="flex items-center gap-2 flex-wrap text-xs text-neutral-500">
          <span>Suggestions:</span>
          {filteredSuggestions.map((tag) => (
            <button
              key={tag}
              type="button"
              onClick={() => addTag(tag)}
              disabled={isPending}
              className="px-2 py-1 rounded-md bg-white/5 border border-white/10 hover:border-emerald-400/40 text-neutral-300 transition-colors disabled:opacity-60"
            >
              {tag}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
