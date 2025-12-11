'use client';

import { useMemo, useState, useTransition } from 'react';
import { updateRecipeStatus } from './actions';

interface RecipeStatusControlProps {
  filePath: string;
  status: string;
  recipeId?: string;
  compact?: boolean;
}

const DEFAULT_STATUSES = ['To try', 'Tried', 'Perfected'];

export default function RecipeStatusControl({ filePath, status, recipeId, compact }: RecipeStatusControlProps) {
  const [currentStatus, setCurrentStatus] = useState(status);
  const [isPending, startTransition] = useTransition();

  const options = useMemo(() => {
    const set = new Set(DEFAULT_STATUSES);
    set.add(status);
    return Array.from(set);
  }, [status]);

  const handleChange = (value: string) => {
    setCurrentStatus(value);
    startTransition(async () => {
      const res = await updateRecipeStatus(filePath, value);
      if (!res.success) {
        // Roll back on failure; a toast system would be nicer but keep minimal UI churn.
        setCurrentStatus(status);
      }
    });
  };

  const baseClasses =
    'rounded-lg text-sm focus:outline-none focus:border-emerald-500/50 transition-colors disabled:opacity-60 disabled:cursor-not-allowed';
  const variantClasses = compact
    ? 'bg-neutral-900/60 border border-white/10 px-3 py-1 text-neutral-200'
    : 'bg-neutral-900/50 border border-white/10 px-4 py-2 text-neutral-200';

  return (
    <div className={compact ? 'flex items-center gap-2 text-xs text-neutral-500' : 'flex flex-col gap-1'}>
      {!compact && <span className="text-xs text-neutral-500">Status</span>}
      <select
        value={currentStatus}
        disabled={isPending}
        onChange={(e) => handleChange(e.target.value)}
        className={`${baseClasses} ${variantClasses}`}
        aria-label="Recipe status"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}
