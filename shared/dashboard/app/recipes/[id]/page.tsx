import { getRecipe, getRecipes } from '@/lib/api';
import { Clock, Users, Flame, ChevronLeft, Tags } from 'lucide-react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import RecipeStatusControl from '../RecipeStatusControl';
import RecipeTagsEditor from '../RecipeTagsEditor';

export default async function RecipeDetail({ params }: { params: { id: string } }) {
  const { id } = await params;
  const recipes = await getRecipes();
  const recipe = recipes.find((r) => r.id === id);
  if (!recipe) notFound();

  const tagSuggestions = Array.from(
    new Set(
      recipes
        .flatMap((r) => r.tags || [])
        .filter(Boolean)
    )
  ).sort((a, b) => a.localeCompare(b));

  // Theme logic ported from python
  const getTheme = (tags: string[] = [], type: string = '') => {
    const t = [...tags, type].map(s => s.toLowerCase());
    if (t.includes('ninja')) return { accent: 'emerald', bg: 'from-slate-900 to-zinc-900', icon: '🔥' };
    if (t.includes('soup')) return { accent: 'amber', bg: 'from-amber-950 to-orange-950', icon: '🍲' };
    if (t.includes('tomato')) return { accent: 'red', bg: 'from-red-950 to-orange-950', icon: '🍅' };
    if (t.includes('meat')) return { accent: 'rose', bg: 'from-rose-950 to-red-950', icon: '🥩' };
    return { accent: 'emerald', bg: 'from-neutral-900 to-neutral-950', icon: '🍳' };
  };

  const theme = getTheme(recipe.tags, recipe.type);

  return (
    <div className={`min-h-screen -m-8 p-8 bg-gradient-to-br ${theme.bg}`}>
      <Link href="/recipes" className="inline-flex items-center text-neutral-400 hover:text-white mb-8 transition-colors">
        <ChevronLeft className="w-4 h-4 mr-1" />
        Back to collection
      </Link>

      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="glass-panel p-8 md:p-12 mb-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 text-9xl opacity-5 transform translate-x-10 -translate-y-4 group-hover:scale-110 transition-transform duration-700">
                {recipe.icon || theme.icon}
            </div>
            
            <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4 flex-wrap justify-between">
                    <span className="text-5xl shadow-xl">{recipe.icon || theme.icon}</span>
                    <div className="flex items-center gap-2 flex-wrap">
                        {recipe.type && (
                            <span className="bg-white/10 px-3 py-1 rounded-full text-sm font-medium border border-white/5 backdrop-blur-md">
                                {recipe.type}
                            </span>
                        )}
                        <RecipeStatusControl filePath={recipe.filePath} status={recipe.status} />
                    </div>
                </div>
                <h1 className="text-4xl md:text-5xl font-bold text-white mb-2 tracking-tight">{recipe.name}</h1>
                <p className="text-xl text-neutral-400 font-light">{recipe.name_en}</p>
            </div>
        </div>

        {/* Meta Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="glass-panel p-4 flex flex-col items-center justify-center text-center">
                <Users className={`w-6 h-6 mb-2 text-${theme.accent}-400`} />
                <div className="text-sm text-neutral-400">Servings</div>
                <div className="font-bold text-lg">{recipe.servings || '-'}</div>
            </div>
            <div className="glass-panel p-4 flex flex-col items-center justify-center text-center">
                <Clock className="w-6 h-6 mb-2 text-blue-400" />
                <div className="text-sm text-neutral-400">Prep</div>
                <div className="font-bold text-lg">{recipe.prep_time || '-'}</div>
            </div>
            <div className="glass-panel p-4 flex flex-col items-center justify-center text-center">
                <Flame className="w-6 h-6 mb-2 text-orange-400" />
                <div className="text-sm text-neutral-400">Cook</div>
                <div className="font-bold text-lg">{recipe.cook_time || '-'}</div>
            </div>
            <div className="glass-panel p-4 flex flex-col items-center justify-center text-center">
                <div className="text-2xl mb-1">📋</div>
                <div className="text-sm text-neutral-400">Status</div>
                <div className="font-bold text-lg text-emerald-400">{recipe.status}</div>
            </div>
        </div>

        <div className="glass-panel p-6 mb-8">
            <div className="flex items-center gap-2 mb-3 text-neutral-300">
                <Tags className="w-4 h-4" />
                <span className="font-semibold text-sm">Tags</span>
            </div>
            <RecipeTagsEditor filePath={recipe.filePath} initialTags={recipe.tags || []} suggestions={tagSuggestions} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Ingredients */}
            <div className="md:col-span-1">
                <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                    <span className="text-emerald-400">🥗</span> Ingredients
                </h2>
                <div className="space-y-3">
                    {recipe.ingredients.map((item, idx) => (
                        <div key={idx} className="glass-panel p-3 text-neutral-300 text-sm flex items-start gap-3 hover:bg-white/5 transition-colors">
                            <span className="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">
                                {idx + 1}
                            </span>
                            {item}
                        </div>
                    ))}
                </div>
            </div>

            {/* Instructions */}
            <div className="md:col-span-2">
                <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                    <span className="text-amber-400">👨‍🍳</span> Instructions
                </h2>
                <div className="space-y-6">
                    {recipe.instructions.map((step, idx) => (
                        <div key={idx} className="flex gap-4 group">
                            <div className={`w-8 h-8 rounded-full bg-gradient-to-br from-${theme.accent}-500 to-${theme.accent}-700 flex items-center justify-center text-white font-bold text-sm shadow-lg flex-shrink-0 mt-1 ring-2 ring-white/10 group-hover:scale-110 transition-transform`}>
                                {idx + 1}
                            </div>
                            <div className="glass-panel p-6 flex-1 text-neutral-300 leading-relaxed text-lg">
                                {step}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Notes */}
                {recipe.notes && recipe.notes.length > 0 && (
                    <div className="mt-12">
                        <h2 className="text-xl font-semibold mb-4 text-neutral-400">📝 Notes</h2>
                        <div className="space-y-4">
                            {recipe.notes.map((note, idx) => (
                                <div key={idx} className="bg-yellow-900/20 border border-yellow-700/30 p-4 rounded-xl text-yellow-200/80 text-sm flex gap-3">
                                    <span>💡</span>
                                    {note}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
      </div>
    </div>
  );
}
