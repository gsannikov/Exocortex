import { getJobs, getSystemStats, getActivityFeed } from '@/lib/api';
import { Briefcase, Zap, ArrowUpRight, Activity } from 'lucide-react';
import Link from 'next/link';

export default async function Dashboard() {
  const jobs = await getJobs();
  const system = await getSystemStats();
  const activities = await getActivityFeed();
  

  const interviewCount = jobs.filter(j => j.status === 'interviewing').length;
  
  return (
    <div className="space-y-10">
      <header className="mb-6">
        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-neutral-200 to-neutral-400 mb-2">
          Command Center
        </h1>
        <p className="text-neutral-400 text-base">Overview of your augmented operations</p>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        <Link href="/career">
            <StatCard 
                title="Jobs Pipeline" 
                value={jobs.length} 
                subtitle={`${interviewCount} interviewing`}
                icon={Briefcase}
                accent="cyan" 
            />
        </Link>
        <StatCard 
            title="Knowledge Load" 
            value={`${system.cpu}%`} 
            subtitle="Capacity utilization"
            icon={Zap}
            accent="purple" 
        />
        <StatCard 
            title="Memory Usage" 
            value={`${Math.round(system.memory)}MB`} 
            subtitle="Heap allocation"
            icon={Activity}
            accent="green" 
        />
        <Link href="/recipes" className="glass-panel p-6 flex flex-col justify-between items-start bg-gradient-to-br from-emerald-900/40 to-black hover:border-emerald-500/30 hover:shadow-lg hover:shadow-emerald-500/10 transition-all cursor-pointer group h-full">
             <div className="w-full">
                <h3 className="text-neutral-400 text-sm font-medium mb-2">Culinary</h3>
                <div className="text-2xl font-semibold text-white group-hover:text-emerald-300 transition-colors mb-1">Recipe DB</div>
                <div className="text-xs text-neutral-500">Recipe collection</div>
             </div>
             <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center group-hover:bg-emerald-500 group-hover:text-white transition-all mt-4">
                <ArrowUpRight className="w-5 h-5" />
             </div>
        </Link>
      </div>

      {/* Main Content Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
         {/* Left: Activity Feed */}
         <div className="lg:col-span-2 space-y-5">
             <div className="flex items-center justify-between mb-1">
                <h2 className="text-xl font-semibold text-white">Latest Activity</h2>
                <span className="text-xs text-neutral-500">{activities.length} items</span>
             </div>
             
             <div className="space-y-3">
                {activities.map(item => (
                    <Link key={item.id} href={item.url || '#'} className="block">
                        <div className="glass-panel p-5 flex items-center gap-4 hover:bg-white/5 hover:border-white/20 transition-all group cursor-pointer">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 transition-transform group-hover:scale-110 ${
                                item.type === 'job' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
                                item.type === 'idea' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                                'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            }`}>
                                {item.type === 'job' ? <Briefcase className="w-6 h-6" /> :
                                 item.type === 'idea' ? <Zap className="w-6 h-6" /> :
                                 <Zap className="w-6 h-6" />}
                            </div>
                            <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between mb-1.5">
                                    <span className="text-sm font-medium text-neutral-300">{item.action}</span>
                                    <span className="text-xs text-neutral-500">{new Date(item.date).toLocaleDateString()}</span>
                                </div>
                                <div className="font-medium text-white truncate group-hover:text-cyan-300 transition-colors">{item.title}</div>
                            </div>
                            <div className="opacity-0 group-hover:opacity-100 p-2 hover:bg-white/10 rounded-lg transition-all text-neutral-400 group-hover:text-white">
                                <ArrowUpRight className="w-4 h-4" />
                            </div>
                        </div>
                    </Link>
                ))}
                {activities.length === 0 && (
                    <div className="glass-panel text-center p-12 text-neutral-500">
                        <Activity className="w-12 h-12 mx-auto mb-3 opacity-50" />
                        <p>No recent activity found</p>
                    </div>
                )}
             </div>
         </div>
         
         {/* Right: Quick Actions */}
         <div className="space-y-5">
            <div className="flex items-center justify-between mb-1">
                <h2 className="text-xl font-semibold text-white">Quick Actions</h2>
            </div>
            <div className="space-y-3">
                <Link href="/career" className="glass-panel p-4 hover:bg-white/5 hover:border-cyan-500/30 transition-all flex items-center gap-3 group">
                    <div className="w-10 h-10 rounded-lg bg-cyan-500/10 flex items-center justify-center group-hover:bg-cyan-500/20 transition-colors">
                        <Briefcase className="w-5 h-5 text-cyan-400" />
                    </div>
                    <span className="font-medium text-sm">View Job Database</span>
                </Link>
                <Link href="/ideas" className="glass-panel p-4 hover:bg-white/5 hover:border-amber-500/30 transition-all flex items-center gap-3 group">
                    <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center group-hover:bg-amber-500/20 transition-colors">
                        <Zap className="w-5 h-5 text-amber-400" />
                    </div>
                    <span className="font-medium text-sm">Capture New Idea</span>
                </Link>
                <div className="glass-panel p-4 opacity-50 cursor-not-allowed flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-neutral-500/10 flex items-center justify-center">
                        <Activity className="w-5 h-5 text-gray-400" />
                    </div>
                    <span className="font-medium text-sm">System Diagnostics</span>
                    <span className="ml-auto text-xs text-neutral-600">Coming Soon</span>
                </div>
            </div>
         </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, icon: Icon, accent }: any) {
    const colors = {
        cyan: {
            icon: 'text-cyan-400 bg-cyan-400/10 border-cyan-400/20',
            hover: 'hover:border-cyan-400/40 hover:shadow-lg hover:shadow-cyan-500/10'
        },
        purple: {
            icon: 'text-purple-400 bg-purple-400/10 border-purple-400/20',
            hover: 'hover:border-purple-400/40 hover:shadow-lg hover:shadow-purple-500/10'
        },
        green: {
            icon: 'text-green-400 bg-green-400/10 border-green-400/20',
            hover: 'hover:border-green-400/40 hover:shadow-lg hover:shadow-green-500/10'
        },
    };
    const colorScheme = colors[accent as keyof typeof colors] || colors.cyan;

    return (
        <div className={`glass-panel p-6 hover:shadow-xl transition-all duration-300 h-full ${colorScheme.hover}`}>
            <div className="flex justify-between items-start mb-5">
                <div className={`p-3 rounded-xl border ${colorScheme.icon}`}>
                    <Icon className="w-6 h-6" />
                </div>
            </div>
            <div className="text-3xl font-bold mb-2 tracking-tight text-white">{value}</div>
            <div className="text-sm font-medium text-neutral-400 mb-1">{title}</div>
            <div className="text-xs text-neutral-500">{subtitle}</div>
        </div>
    )
}
