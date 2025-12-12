'use client';

import { FolderOpen } from 'lucide-react';
import { openCollateralInEditor } from '../app/actions';
import { useState } from 'react';

export default function OpenCollateralButton() {
  const [isOpening, setIsOpening] = useState(false);

  const handleOpen = async () => {
    setIsOpening(true);
    try {
      await openCollateralInEditor();
    } catch (error) {
      console.error('Failed to open collateral:', error);
    } finally {
      setIsOpening(false);
    }
  };

  return (
    <button
      onClick={handleOpen}
      disabled={isOpening}
      className="flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all text-neutral-400 hover:text-white hover:bg-white/5 w-full text-left disabled:opacity-50 disabled:cursor-not-allowed"
      title="Open Collateral in Default Editor"
    >
      <FolderOpen className="w-5 h-5" />
      <span className="text-sm font-medium">
        {isOpening ? 'Opening...' : 'Open Collateral'}
      </span>
    </button>
  );
}

