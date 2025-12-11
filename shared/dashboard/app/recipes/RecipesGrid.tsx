'use client';

import { useMemo, useState } from 'react';
import { Clock, Users, ArrowRight } from 'lucide-react';
import Link from 'next/link';
import FilterBar from '../../components/FilterBar';
import type { Recipe } from '../../lib/shared-types';
import RecipeStatusControl from './RecipeStatusControl';

interface RecipesGridProps {
  recipes: Recipe[];
}

export default function RecipesGrid({ recipes }: RecipesGridProps) {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');

  const uniqueStatuses = useMemo(() => {
    const set = new Set<string>();
    recipes.forEach((recipe) => recipe.status && set.add(recipe.status));
    return Array.from(set);
  }, [recipes]);

  const uniqueTypes = useMemo(() => {
    const set = new Set<string>();
    recipes.forEach((recipe) => recipe.type && set.add(recipe.type));
    return Array.from(set);
  }, [recipes]);

  const filteredRecipes = useMemo(() => {
    return recipes.filter((recipe) => {
      const haystack = `${recipe.name} ${recipe.name_en || ''} ${(recipe.tags || []).join(' ')}`.toLowerCase();
      const matchesSearch = haystack.includes(search.toLowerCase());
      const matchesStatus = statusFilter === 'all' ? true : recipe.status === statusFilter;
      const matchesType = typeFilter === 'all' ? true : recipe.type === typeFilter;

      return matchesSearch && matchesStatus && matchesType;
    });
  }, [recipes, search, statusFilter, typeFilter]);

  return (
    <div className="space-y-6">
      <FilterBar
        search={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search recipes, tags, or names..."
        filters={[
          {
            value: statusFilter,
            onChange: setStatusFilter,
            label: 'Status',
            options: [
              { label: 'All statuses', value: 'all' },
              ...uniqueStatuses.map((status) => ({ label: status, value: status })),
            ],
          },
          {
            value: typeFilter,
            onChange: setTypeFilter,
            label: 'Type',
            options: [
              { label: 'All types', value: 'all' },
              ...uniqueTypes.map((type) => ({ label: type, value: type })),
            ],
          },
        ]}
      />

      {filteredRecipes.length === 0 ? (
        <div className="glass-panel text-center p-12 text-neutral-500">
          <p className="text-sm">No recipes match your search or filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredRecipes.map((recipe) => (
            <Link key={recipe.id} href={`/recipes/${recipe.id}`} className="group">
              <div className="glass-panel p-6 h-full hover:border-emerald-500/30 transition-all hover:bg-white/5 flex flex-col">
                <div className="flex justify-between items-start mb-4 gap-3">
                  <div className="text-4xl flex-shrink-0">{recipe.icon || '🍳'}</div>
                  <RecipeStatusControl filePath={recipe.filePath} status={recipe.status} compact />
                </div>

                <h3 className="text-xl font-bold mb-1 group-hover:text-emerald-300 transition-colors">
                  {recipe.name}
                </h3>
                <p className="text-neutral-500 text-sm mb-4">{recipe.name_en}</p>

                <div className="flex items-center gap-4 mt-auto text-sm text-neutral-400">
                  {recipe.prep_time && (
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5" />
                      {recipe.prep_time}
                    </div>
                  )}
                  {recipe.servings && (
                    <div className="flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5" />
                      {recipe.servings}
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-white/5 flex justify-between items-center text-xs text-neutral-500">
                  <div className="flex gap-2">
                    {recipe.tags?.slice(0, 2).map((tag) => (
                      <span key={tag} className="bg-white/5 px-2 py-0.5 rounded">
                        #{tag}
                      </span>
                    ))}
                  </div>
                  <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity text-emerald-400" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
