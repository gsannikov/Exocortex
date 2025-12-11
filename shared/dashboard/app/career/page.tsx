import DashboardWidget from '../../components/DashboardWidget';
import { Briefcase, Building, Clock, CheckCircle } from 'lucide-react';

export default function CareerPage() {
  return (
    <div className="space-y-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Job Search & Career</h1>
        <p className="text-neutral-400">Track applications, analyze opportunities, and manage your pipeline.</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-[600px]">
        {/* Applied Column */}
        <DashboardWidget title="Applied" icon={Briefcase} className="border-l-4 border-l-blue-500">
          <div className="space-y-4">
            <JobCard 
              company="Anthropic" 
              role="Product Engineer" 
              date="2d ago" 
              status="Applied"
            />
            <JobCard 
              company="OpenAI" 
              role="Member of Technical Staff" 
              date="3d ago" 
              status="Applied"
            />
            <JobCard 
              company="Google DeepMind" 
              role="Research Engineer" 
              date="5d ago" 
              status="Applied"
            />
          </div>
        </DashboardWidget>

        {/* In Progress Column */}
        <DashboardWidget title="In Progress" icon={Clock} className="border-l-4 border-l-yellow-500">
          <div className="space-y-4">
             <JobCard 
              company="Linear" 
              role="Senior Frontend Engineer" 
              date="1w ago" 
              status="Interviewing"
              badge="Tech Round"
              accent="yellow"
            />
          </div>
        </DashboardWidget>

        {/* Offers Column */}
        <DashboardWidget title="Offers" icon={CheckCircle} className="border-l-4 border-l-green-500">
          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-green-900/20 border border-green-500/30 text-center">
              <Building className="w-8 h-8 text-green-400 mx-auto mb-2" />
              <div className="font-bold text-green-400">Offer Received</div>
              <div className="text-sm text-neutral-400">Vercel - Sr. Eng</div>
            </div>
          </div>
        </DashboardWidget>
      </div>
    </div>
  );
}

function JobCard({ company, role, date, status, badge, accent = 'blue' }: any) {
  return (
    <div className="p-3 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors cursor-pointer">
      <div className="flex justify-between items-start mb-2">
        <div className="font-medium">{company}</div>
        <div className="text-xs text-neutral-500">{date}</div>
      </div>
      <div className="text-sm text-neutral-300 mb-3">{role}</div>
      <div className="flex items-center gap-2">
         {badge && (
            <span className={`text-[10px] px-2 py-0.5 rounded-full bg-${accent}-500/20 text-${accent}-400 border border-${accent}-500/20`}>
              {badge}
            </span>
         )}
         <span className="text-[10px] px-2 py-0.5 rounded-full bg-neutral-800 text-neutral-400 border border-neutral-700">
            {status}
         </span>
      </div>
    </div>
  )
}
