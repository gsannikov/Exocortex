import DashboardWidget from '../../components/DashboardWidget';
import { Search, FileText, Upload } from 'lucide-react';

export default function RagPage() {
  return (
    <div className="space-y-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Local Knowledge Base</h1>
        <p className="text-neutral-400">Search and manage your indexed local documents.</p>
      </header>
      
      {/* Search Bar */}
      <div className="relative mb-8">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-500 w-5 h-5" />
        <input 
            type="text" 
            placeholder="Search your knowledge base..." 
            className="w-full bg-neutral-900/50 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-lg focus:outline-none focus:border-purple-500/50 transition-colors"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stats */}
        <div className="lg:col-span-2 space-y-6">
            <DashboardWidget title="Recent Ingestions" icon={FileText}>
                <div className="space-y-0 divide-y divide-white/5">
                    {[1,2,3,4,5].map((i) => (
                        <div key={i} className="py-3 flex items-center justify-between group cursor-pointer hover:bg-white/5 px-2 rounded-lg -mx-2 transition-colors">
                            <div className="flex items-center gap-3">
                                <div className="p-2 bg-blue-500/10 rounded-lg text-blue-400">
                                    <FileText className="w-4 h-4" />
                                </div>
                                <div>
                                    <div className="text-sm font-medium group-hover:text-blue-400 transition-colors">Document_Analysis_v{i}.pdf</div>
                                    <div className="text-xs text-neutral-500">/Users/gursannikov/Documents/Work</div>
                                </div>
                            </div>
                            <div className="text-xs text-neutral-500">2h ago</div>
                        </div>
                    ))}
                </div>
            </DashboardWidget>
        </div>

        {/* Status */}
        <div className="space-y-6">
             <div className="glass-panel p-6 bg-green-500/5 border-green-500/20">
                <h3 className="text-sm font-medium text-green-400 mb-1">System Status</h3>
                <div className="text-2xl font-bold mb-4">Online</div>
                
                <div className="space-y-4">
                    <div>
                        <div className="flex justify-between text-xs mb-1">
                            <span className="text-neutral-400">Vector Store</span>
                            <span className="text-green-400">Healthy</span>
                        </div>
                        <div className="h-1 bg-neutral-800 rounded-full overflow-hidden">
                            <div className="h-full bg-green-500 w-full"></div>
                        </div>
                    </div>
                     <div>
                        <div className="flex justify-between text-xs mb-1">
                            <span className="text-neutral-400">Embedding Model</span>
                            <span className="text-green-400">Loaded</span>
                        </div>
                         <div className="h-1 bg-neutral-800 rounded-full overflow-hidden">
                            <div className="h-full bg-green-500 w-full"></div>
                        </div>
                    </div>
                </div>
            </div>

             <DashboardWidget title="Quick Actions" icon={Upload}>
                <div className="grid grid-cols-2 gap-3">
                    <button className="p-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs font-medium transition-colors">
                        Re-index All
                    </button>
                    <button className="p-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs font-medium transition-colors">
                        Add Source
                    </button>
                </div>
             </DashboardWidget>
        </div>
      </div>
    </div>
  );
}
