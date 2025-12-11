'use client';

import { useMemo, useState } from 'react';
import { BookOpen, ExternalLink, CheckCircle, Clock } from 'lucide-react';
import DashboardWidget from '../../components/DashboardWidget';
import ActionButtons from '../../components/ActionButtons';
import FilterBar from '../../components/FilterBar';
import type { ReadingItem } from '../../lib/shared-types';

type StatusFilter = 'all' | 'queued' | 'reading' | 'done';

function isQueued(status?: string) {
  return status === 'to_read' || status === 'unread' || !status;
}

export default function ReadingBoard({ items }: { items: ReadingItem[] }) {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');

  const filtered = useMemo(() => {
    return items.filter((item) => {
      const haystack = `${item.title} ${item.url} ${item.summary || ''}`.toLowerCase();
      const matchesSearch = haystack.includes(search.toLowerCase());
      const matchesStatus =
        statusFilter === 'all'
          ? true
          : statusFilter === 'queued'
          ? isQueued(item.status)
          : item.status === statusFilter;

      return matchesSearch && matchesStatus;
    });
  }, [items, search, statusFilter]);

  const toRead = filtered.filter((item) => isQueued(item.status));
  const reading = filtered.filter((item) => item.status === 'reading');
  const done = filtered.filter((item) => item.status === 'done');

  return (
    <div className="space-y-8">
      <header className="mb-2">
        <h1 className="text-4xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-300">
          Reading List
        </h1>
        <p className="text-neutral-400 text-base mb-2">Curated articles, papers, and books for deep work.</p>
        <div className="flex flex-wrap gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-500"></div>
            <span className="text-neutral-500">{toRead.length} to read</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
            <span className="text-neutral-500">{reading.length} in progress</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-500"></div>
            <span className="text-neutral-500">{done.length} finished</span>
          </div>
        </div>
      </header>

      <FilterBar
        search={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search reading list..."
        filters={[
          {
            value: statusFilter,
            onChange: (value) => setStatusFilter(value as StatusFilter),
            label: 'Status',
            options: [
              { label: 'All items', value: 'all' },
              { label: 'Queued', value: 'queued' },
              { label: 'In Progress', value: 'reading' },
              { label: 'Finished', value: 'done' },
            ],
          },
        ]}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
        <DashboardWidget title="To Read" icon={BookOpen}>
          <div className="space-y-3">
            {toRead.length === 0 && (
              <div className="glass-panel text-center p-8 text-neutral-500">
                <BookOpen className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p className="text-sm italic">No items queued.</p>
              </div>
            )}
            {toRead.map((item) => (
              <ReadingCard key={item.url} item={item} />
            ))}
          </div>
        </DashboardWidget>

        <div className="space-y-6 lg:space-y-8">
          <DashboardWidget title="In Progress" icon={Clock} className="border-l-4 border-l-yellow-500/50">
            <div className="space-y-3">
              {reading.length === 0 && (
                <div className="glass-panel text-center p-8 text-neutral-500">
                  <Clock className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm italic">Nothing currently in progress.</p>
                </div>
              )}
              {reading.map((item) => (
                <ReadingCard key={item.url} item={item} accent="yellow" />
              ))}
            </div>
          </DashboardWidget>
          <DashboardWidget title="Finished" icon={CheckCircle} className="opacity-75">
            <div className="space-y-3">
              {done.length === 0 && (
                <div className="glass-panel text-center p-8 text-neutral-500">
                  <CheckCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm italic">Nothing finished yet.</p>
                </div>
              )}
              {done.map((item) => (
                <ReadingCard key={item.url} item={item} accent="green" />
              ))}
            </div>
          </DashboardWidget>
        </div>
      </div>
    </div>
  );
}

function ReadingCard({ item, accent }: { item: ReadingItem; accent?: 'yellow' | 'green' }) {
  const accentColors = {
    yellow: 'border-l-yellow-500/30 hover:border-l-yellow-500/50',
    green: 'border-l-green-500/30 hover:border-l-green-500/50',
  };
  const borderClass = accent ? accentColors[accent] : 'border-l-blue-500/30 hover:border-l-blue-500/50';

  return (
    <div className={`p-5 glass-panel border-l-4 ${borderClass} hover:bg-white/5 transition-all relative group`}>
      <div className="absolute top-3 right-3 z-10">
        <ActionButtons filePath={item.filePath} />
      </div>
      <div className="pr-10">
        <h3 className="font-semibold text-lg mb-2 leading-snug group-hover:text-cyan-300 transition-colors">
          {item.title}
        </h3>
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-blue-400 hover:text-blue-300 hover:underline flex items-center gap-1.5 mb-3 transition-colors"
        >
          <span className="truncate max-w-[200px]">{item.url}</span>
          <ExternalLink className="w-3.5 h-3.5 flex-shrink-0" />
        </a>
        {item.summary && <p className="text-sm text-neutral-400 line-clamp-3 leading-relaxed">{item.summary}</p>}
      </div>
    </div>
  );
}
