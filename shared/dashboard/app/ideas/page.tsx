import DashboardWidget from '../../components/DashboardWidget';
import { Lightbulb, Plus, Star } from 'lucide-react';

export default function IdeasPage() {
  return (
    <div className="space-y-8">
      <header className="flex justify-between items-end mb-8">
        <div>
            <h1 className="text-3xl font-bold mb-2">Ideas & Notes</h1>
            <p className="text-neutral-400">Capture, organize, and develop your thoughts.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg transition-colors font-medium">
            <Plus className="w-4 h-4" />
            New Idea
        </button>
      </header>

      {/* Masonry Grid (Mocked with columns for now) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
            { title: "AI-Powered Garden Monitor", tag: "Project", color: "purple" },
            { title: "Recipe: Spicy Tuna Poke", tag: "Food", color: "orange" },
            { title: "Book Idea: The Last Algorithm", tag: "Writing", color: "blue" },
            { title: "Dashboard Architecture v2", tag: "Dev", color: "green" },
            { title: "Gift Ideas for Mom", tag: "Personal", color: "pink" },
            { title: "React Context Optimization", tag: "Dev", color: "green" },
        ].map((idea, i) => (
            <div key={i} className="glass-panel p-6 hover:border-purple-500/30 transition-colors group cursor-pointer h-min break-inside-avoid">
                <div className="flex justify-between items-start mb-4">
                    <span className={`px-2 py-1 rounded-md bg-${idea.color}-500/10 text-${idea.color}-400 text-xs font-medium border border-${idea.color}-500/20`}>
                        {idea.tag}
                    </span>
                    <Star className="w-4 h-4 text-neutral-600 group-hover:text-yellow-400 transition-colors" />
                </div>
                <h3 className="text-lg font-semibold mb-2 group-hover:text-purple-300 transition-colors">{idea.title}</h3>
                <p className="text-sm text-neutral-400 line-clamp-3">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                </p>
                <div className="mt-4 pt-4 border-t border-white/5 text-xs text-neutral-600 flex justify-between">
                    <span>Oct {20 - i}</span>
                    <span>12kb</span>
                </div>
            </div>
        ))}
      </div>
    </div>
  );
}
