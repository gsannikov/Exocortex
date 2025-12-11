import fs from 'fs/promises';
import path from 'path';
import yaml from 'yaml';
import { DATA_PATHS } from './paths';

export interface JobAnalysis {
  id: string;
  title: string;
  company: string;
  status: 'applied' | 'interviewing' | 'offer' | 'rejected' | 'backlog';
  score?: number;
  added_at: string;
}

export async function getJobs(): Promise<JobAnalysis[]> {
  try {
    // Check if dir exists
    console.log(`[API] Checking jobs path: ${DATA_PATHS.analyses}`);
    try {
      await fs.access(DATA_PATHS.analyses);
    } catch {
      console.warn(`[API] Path not found: ${DATA_PATHS.analyses}`);
      return [];
    }

    const files = await fs.readdir(DATA_PATHS.analyses);
    console.log(`[API] Found ${files.length} files`);
    const jobs: JobAnalysis[] = [];

    for (const file of files) {
      if (!file.endsWith('.yaml')) continue;
      
      const filePath = path.join(DATA_PATHS.analyses, file);
      const content = await fs.readFile(filePath, 'utf-8');
      const data = yaml.parse(content);
      
      jobs.push({
        id: data.id || file.replace('.yaml', ''),
        title: data.title || 'Unknown Role',
        company: data.company || 'Unknown Company',
        status: data.status || 'backlog',
        score: data.analysis?.score || 0,
        added_at: data.added_at || new Date().toISOString()
      });
    }
    
    // Sort by date desc
    return jobs.sort((a, b) => new Date(b.added_at).getTime() - new Date(a.added_at).getTime());
  } catch (error) {
    console.error('Error fetching jobs:', error);
    return [];
  }
}

export async function getSystemStats() {
    // Mock for MVP
    return {
        status: 'Operational',
        uptime: '99.9%',
        cpu: 12,
        memory: 34
    }
}
