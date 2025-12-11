import type { Metadata } from 'next';
import './globals.css';
import { LayoutDashboard, BookOpen, Mic, Lightbulb, Activity, Briefcase, Users, Database, Utensils, Share2, Code, Settings } from 'lucide-react';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Exocortex | Dashboard',
  description: 'AI Augmentation Command Center',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex h-screen bg-black text-white overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 border-r border-white/10 p-6 flex flex-col gap-8 bg-neutral-950/50 backdrop-blur-md">
            <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-cyan-400 to-purple-600 flex items-center justify-center">
                    <Activity className="w-5 h-5 text-white" />
                </div>
                <span className="font-bold text-lg tracking-tight">Exocortex</span>
            </div>

            <nav className="flex flex-col gap-2 overflow-y-auto flex-1 pr-2">
                <div className="text-xs font-medium text-neutral-500 mt-4 mb-2 uppercase tracking-wider px-3">Overview</div>
                <NavItem icon={LayoutDashboard} label="Command Center" href="/" active />

                <div className="text-xs font-medium text-neutral-500 mt-4 mb-2 uppercase tracking-wider px-3">Career & Growth</div>
                <NavItem icon={Briefcase} label="Job Search" href="/career" />
                <NavItem icon={Users} label="Interview Prep" href="/career/interview" />
                
                <div className="text-xs font-medium text-neutral-500 mt-4 mb-2 uppercase tracking-wider px-3">Knowledge Base</div>
                <NavItem icon={BookOpen} label="Reading List" href="/reading" />
                <NavItem icon={Database} label="Local RAG" href="/rag" />
                <NavItem icon={Lightbulb} label="Ideas" href="/ideas" />
                <NavItem icon={Mic} label="Voice Memos" href="/voice" />

                <div className="text-xs font-medium text-neutral-500 mt-4 mb-2 uppercase tracking-wider px-3">Lifestyle</div>
                <NavItem icon={Utensils} label="Recipes" href="/recipes" />
                <NavItem icon={Share2} label="Social Posts" href="/social" />

                <div className="text-xs font-medium text-neutral-500 mt-4 mb-2 uppercase tracking-wider px-3">System</div>
                <NavItem icon={Code} label="Generator" href="/generator" />
                <NavItem icon={Settings} label="Setup & Health" href="/setup" />
            </nav>

            <div className="mt-auto pt-6 border-t border-white/5">
                <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-white/5">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-sm font-medium text-neutral-400">System Online</span>
                </div>
            </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-8 relative">
            <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-purple-900/20 to-transparent pointer-events-none" />
            <div className="relative z-10 max-w-7xl mx-auto">
                {children}
            </div>
        </main>
      </body>
    </html>
  );
}

function NavItem({ icon: Icon, label, href, active }: any) {
    return (
        <Link href={href} className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${active ? 'bg-white/10 text-white shadow-lg shadow-purple-500/10' : 'text-neutral-400 hover:text-white hover:bg-white/5'}`}>
            <Icon className="w-5 h-5" />
            <span className="text-sm font-medium">{label}</span>
        </Link>
    )
}
