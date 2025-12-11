import fs from 'fs/promises';
import path from 'path';
import yaml from 'yaml';
import { DATA_PATHS } from '../paths';
import type { ReadingItem } from '../shared-types';

export async function getReadingList(): Promise<ReadingItem[]> {
    try {
        const filePath = path.join(DATA_PATHS.readingList, 'reading-list.yaml');
        const content = await fs.readFile(filePath, 'utf-8');
        const data = yaml.parse(content);

        // YAML may be an array of items or an object with { stats, items }
        const items = Array.isArray(data) ? data : (data?.items || []);

        return items.map((item: any) => ({
            ...item,
            filePath // Point to main list file for now
        }));
    } catch (e) {
        console.error('Error in getReadingList:', e);
        return [];
    }
}
