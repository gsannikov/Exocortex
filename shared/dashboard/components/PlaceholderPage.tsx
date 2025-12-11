import { Construction } from 'lucide-react';

export default function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
      <div className="p-4 rounded-full bg-neutral-900 border border-neutral-800">
        <Construction className="w-8 h-8 text-neutral-500" />
      </div>
      <h1 className="text-2xl font-bold">{title}</h1>
      <p className="text-neutral-400 max-w-md">
        This skill module is currently being integrated into the dashboard.
        <br />
        Check back in the next release.
      </p>
    </div>
  );
}
