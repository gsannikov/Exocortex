import { getRecipes } from '@/lib/api';
import RecipesGrid from './RecipesGrid';

export default async function RecipesPage() {
  const recipes = await getRecipes();

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-400">
          Recipe Collection
        </h1>
        <p className="text-neutral-400 mt-1">{recipes.length} culinary algorithms</p>
      </header>

      <RecipesGrid recipes={recipes} />
    </div>
  );
}
