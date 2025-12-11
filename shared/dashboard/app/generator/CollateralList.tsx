'use client';

import { useMemo, useState } from 'react';
import ActionButtons from '../../components/ActionButtons';
import { FileText } from 'lucide-react';
import type { CollateralFile } from '../../lib/services/collateral';
import FilterBar from '../../components/FilterBar';

interface CollateralListProps {
  files: CollateralFile[];
}

export default function CollateralList({ files }: CollateralListProps) {
  const [search, setSearch] = useState('');

  const filteredFiles = useMemo(() => {
    return files.filter((file) => {
      const haystack = `${file.name} ${file.filePath}`.toLowerCase();
      return haystack.includes(search.toLowerCase());
    });
  }, [files, search]);

  if (files.length === 0) {
    return (
      <div className="glass-panel text-center p-8 text-neutral-500">
        <FileText className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm italic">No collateral files found.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <FilterBar
        search={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search collateral files..."
        filters={[]}
      />

      {filteredFiles.length === 0 && (
        <div className="glass-panel text-center p-6 text-neutral-500">
          <p className="text-sm">No files match your search.</p>
        </div>
      )}

      {filteredFiles.map((file) => (
        <div
          key={file.filePath}
          className="glass-panel p-4 hover:bg-white/5 transition-all relative group border-l-4 border-l-cyan-500/30 hover:border-l-cyan-500/50"
        >
          <div className="absolute top-3 right-3 z-10">
            <ActionButtons filePath={file.filePath} />
          </div>
          <div className="pr-10">
            <h3 className="font-semibold text-base mb-1 group-hover:text-cyan-300 transition-colors">
              {file.name}
            </h3>
            <p className="text-xs text-neutral-500 font-mono truncate">
              {file.filePath}
            </p>
            <div className="flex items-center gap-3 mt-2 text-xs text-neutral-500">
              <span>{(file.size / 1024).toFixed(1)} KB</span>
              <span>•</span>
              <span>{file.modified.toLocaleDateString()}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
