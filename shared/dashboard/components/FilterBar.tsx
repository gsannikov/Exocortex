'use client';

import { Search } from 'lucide-react';

interface FilterOption {
  label: string;
  value: string;
}

interface FilterConfig {
  value: string;
  onChange: (value: string) => void;
  options: FilterOption[];
  label?: string;
}

interface FilterBarProps {
  search: string;
  onSearchChange: (value: string) => void;
  searchPlaceholder?: string;
  filters?: FilterConfig[];
  className?: string;
}

export default function FilterBar({
  search,
  onSearchChange,
  searchPlaceholder = 'Search...',
  filters = [],
  className = '',
}: FilterBarProps) {
  return (
    <div className={`flex flex-col md:flex-row gap-4 justify-between items-center bg-white/5 p-4 rounded-xl border border-white/5 ${className}`}>
      <div className="relative w-full md:w-96">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-500" />
        <input
          type="text"
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder={searchPlaceholder}
          className="w-full bg-neutral-900/50 border border-white/10 rounded-lg pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-cyan-500/50 transition-colors"
          aria-label="Search"
        />
      </div>

      {filters.length > 0 && (
        <div className="flex gap-4 w-full md:w-auto">
          {filters.map((filter, idx) => (
            <select
              key={idx}
              value={filter.value}
              onChange={(e) => filter.onChange(e.target.value)}
              className="bg-neutral-900/50 border border-white/10 rounded-lg px-4 py-2 text-sm text-neutral-300 focus:outline-none focus:border-cyan-500/50 transition-colors"
              aria-label={filter.label || 'Filter'}
            >
              {filter.options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          ))}
        </div>
      )}
    </div>
  );
}
