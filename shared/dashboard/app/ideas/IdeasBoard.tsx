'use client';

import { useMemo, useState } from 'react';
import { Plus, FileText } from 'lucide-react';
import ActionButtons from '../../components/ActionButtons';
import FilterBar from '../../components/FilterBar';
import type { Idea } from '../../lib/shared-types';

interface IdeasBoardProps {
  ideas: Idea[];
}

export default function IdeasBoard({ ideas }: IdeasBoardProps) {
  const [search, setSearch] = useState('');
  const [tagFilter, setTagFilter] = useState('all');

  const tags = useMemo(() => {
    const set = new Set<string>();
    ideas.forEach((idea) => idea.tags?.forEach((tag) => set.add(tag)));
    return Array.from(set).sort((a, b) => a.localeCompare(b));
  }, [ideas]);

  const filteredIdeas = useMemo(() => {
    return ideas.filter((idea) => {
      const haystack = `${idea.title} ${idea.content} ${(idea.tags || []).join(' ')}`.toLowerCase();
      const matchesSearch = haystack.includes(search.toLowerCase());
      const matchesTag =
        tagFilter === 'all'
          ? true
          : tagFilter === 'untagged'
          ? !idea.tags || idea.tags.length === 0
          : idea.tags?.includes(tagFilter);

      return matchesSearch && matchesTag;
    });
  }, [ideas, search, tagFilter]);

  return (
    <div className="space-y-8">
      <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 mb-2">
        <div>
          <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-300">
            Ideas & Notes
          </h1>
          <p className="text-neutral-400 text-base">Capture, organize, and develop your thoughts.</p>
          <div className="text-sm text-neutral-500 mt-2">
            {ideas.length} {ideas.length === 1 ? 'idea' : 'ideas'} captured
          </div>
        </div>
        <button className="flex items-center gap-2 px-5 py-2.5 bg-purple-600 hover:bg-purple-500 text-white rounded-lg transition-all font-medium shadow-lg shadow-purple-500/20 hover:shadow-purple-500/30">
          <Plus className="w-4 h-4" />
          New Idea
        </button>
      </header>

      <FilterBar
        search={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search ideas, notes, or tags..."
        filters={[
          {
            value: tagFilter,
            onChange: setTagFilter,
            label: 'Tags',
            options: [
              { label: 'All tags', value: 'all' },
              { label: 'Untagged', value: 'untagged' },
              ...tags.map((tag) => ({ label: tag, value: tag })),
            ],
          },
        ]}
      />

      {filteredIdeas.length === 0 ? (
        <div className="glass-panel text-center p-16">
          <FileText className="w-16 h-16 mx-auto mb-4 text-neutral-600 opacity-50" />
          <h3 className="text-lg font-semibold text-neutral-400 mb-2">No ideas match your filters</h3>
          <p className="text-neutral-500 text-sm">Try adjusting search terms or tag filters.</p>
        </div>
      ) : (
        <div className="columns-1 md:columns-2 lg:columns-3 gap-5 lg:gap-6">
          {filteredIdeas.map((idea) => (
            <div
              key={idea.id}
              className="glass-panel p-6 hover:border-purple-500/30 hover:shadow-lg hover:shadow-purple-500/10 transition-all group cursor-pointer break-inside-avoid relative mb-5"
            >
              <div className="absolute top-3 right-3 z-10">
                <ActionButtons filePath={idea.filePath} />
              </div>
              <div className="flex justify-between items-start mb-4 pr-10">
                <div className="flex gap-2 flex-wrap">
                  {idea.tags && idea.tags.length > 0
                    ? idea.tags.slice(0, 3).map((tag) => (
                        <span
                          key={tag}
                          className="px-2.5 py-1 rounded-md bg-purple-500/10 text-purple-400 text-xs font-medium border border-purple-500/20"
                        >
                          {tag}
                        </span>
                      ))
                    : (
                      <span className="px-2.5 py-1 rounded-md bg-neutral-500/10 text-neutral-400 text-xs font-medium border border-neutral-500/20">
                        Note
                      </span>
                    )}
                  {idea.tags && idea.tags.length > 3 && (
                    <span className="px-2.5 py-1 rounded-md bg-neutral-500/10 text-neutral-500 text-xs font-medium border border-neutral-500/20">
                      +{idea.tags.length - 3}
                    </span>
                  )}
                </div>
              </div>
              <h3 className="text-lg font-semibold mb-3 group-hover:text-purple-300 transition-colors pr-4 leading-snug">
                {idea.title}
              </h3>
              <p className="text-sm text-neutral-400 line-clamp-4 leading-relaxed mb-4">
                {idea.content || 'No content preview available.'}
              </p>
              <div className="pt-4 border-t border-white/5 text-xs text-neutral-500 flex justify-between items-center">
                <span>
                  {new Date(idea.date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric',
                  })}
                </span>
                <FileText className="w-3.5 h-3.5 opacity-50" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
