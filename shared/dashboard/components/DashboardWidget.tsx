import { ReactNode } from 'react';

interface DashboardWidgetProps {
  title: string;
  children: ReactNode;
  icon?: any; // Leaving as any for now to avoid strict type/dep hell, but TODO: fix
  action?: ReactNode;
  className?: string; // Add className prop to the interface
}

export default function DashboardWidget({ title, children, icon: Icon, action, className = "" }: DashboardWidgetProps) {
  return (
    <div className={`glass-panel p-6 flex flex-col h-full ${className}`}> {/* Use template literal to combine classes */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          {Icon && <Icon className="w-5 h-5 text-neutral-400" />}
          <h2 className="text-lg font-semibold">{title}</h2>
        </div>
        {action}
      </div>
      <div className="flex-1 overflow-y-auto">
        {children}
      </div>
    </div>
  );
}
