import { getJobs, getSystemStats } from '@/lib/api';
import { Briefcase, Zap, Clock, ArrowUpRight } from 'lucide-react';

export default async function Dashboard() {
  const jobs = await getJobs();
  const system = await getSystemStats();
  
  const appliedCount = jobs.filter(j => j.status === 'applied').length;
  const interviewCount = jobs.filter(j => j.status === 'interviewing').length;
  
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-neutral-400">
          Command Center
        </h1>
        <p className="text-neutral-400 mt-1">Overview of your augmented operations</p>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard 
            title="Jobs Pipeline" 
            value={jobs.length} 
            subtitle={`${interviewCount} interviewing`}
            icon={Briefcase}
            accent="cyan" 
        />
        <StatCard 
            title="System Load" 
            value={`${system.cpu}%`} 
            subtitle="All systems nominal"
            icon={Zap}
            accent="purple" 
        />
        <StatCard 
            title="Uptime" 
            value={system.uptime} 
            subtitle="Since last reboot"
            icon={Clock}
            accent="green" 
        />
        <div className="glass-panel p-6 flex flex-col justify-between items-start bg-gradient-to-br from-purple-900/40 to-black hover:border-purple-500/30 transition-all cursor-pointer group">
             <div>
                <h3 className="text-neutral-400 text-sm font-medium mb-1">Quick Action</h3>
                <div className="text-xl font-semibold text-white group-hover:text-purple-300 transition-colors">Capture Idea</div>
             </div>
             <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center group-hover:bg-purple-500 group-hover:text-white transition-all">
                <ArrowUpRight className="w-5 h-5" />
             </div>
        </div>
      </div>

      {/* Main Content Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         {/* Left: Job Feed */}
         <div className="lg:col-span-2 space-y-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-cyan-400" />
                Recent Applications
            </h2>
            
            <div className="space-y-4">
                {jobs.length === 0 ? (
                    <div className="glass-panel p-8 text-center text-neutral-500">
                        No job analyses found in <code className="text-xs bg-white/10 px-1 py-0.5 rounded">~/exocortex-data/career/analyses</code>
                    </div>
                ) : (
                    jobs.slice(0, 5).map(job => (
                        <div key={job.id} className="glass-panel p-4 flex items-center justify-between hover:bg-white/5 transition-colors group">
                            <div className="flex items-center gap-4">
                                <div className={`w-2 h-12 rounded-full ${
                                    job.status === 'interviewing' ? 'bg-purple-500' : 
                                    job.status === 'offer' ? 'bg-green-500' :
                                    job.score && job.score > 80 ? 'bg-cyan-500' : 'bg-neutral-800'
                                }`} />
                                <div>
                                    <div className="font-semibold text-lg group-hover:text-cyan-300 transition-colors">{job.title}</div>
                                    <div className="text-sm text-neutral-400">{job.company} • {new Date(job.added_at).toLocaleDateString()}</div>
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                {job.score && (
                                    <div className="text-2xl font-bold text-neutral-700 group-hover:text-white transition-colors">
                                        {job.score}
                                    </div>
                                )}
                                <div className={`px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wider ${
                                    job.status === 'interviewing' ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' :
                                    'bg-white/5 text-neutral-400 border border-white/10'
                                }`}>
                                    {job.status}
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
         </div>

         {/* Right: Activity Log */}
         <div className="space-y-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
                <Clock className="w-5 h-5 text-neutral-400" />
                Latest Activity
            </h2>
            <div className="glass-panel p-6 min-h-[300px] border-dashed border-neutral-800 flex items-center justify-center text-neutral-600">
                Activity feed coming soon...
            </div>
         </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, icon: Icon, accent }: any) {
    const colors = {
        cyan: 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20',
        purple: 'text-purple-400 bg-purple-400/10 border-purple-400/20',
        green: 'text-green-400 bg-green-400/10 border-green-400/20',
    };
    // @ts-ignore
    const colorClass = colors[accent] || colors.cyan;

    return (
        <div className="glass-panel p-6 hover:shadow-2xl hover:shadow-cyan-900/10 transition-all duration-300">
            <div className="flex justify-between items-start mb-4">
                <div className={`p-2 rounded-lg ${colorClass}`}>
                    <Icon className="w-5 h-5" />
                </div>
            </div>
            <div className="text-3xl font-bold mb-1 tracking-tight">{value}</div>
            <div className="text-sm text-neutral-500">{title}</div>
            <div className="text-xs text-neutral-600 mt-2">{subtitle}</div>
        </div>
    )
}
