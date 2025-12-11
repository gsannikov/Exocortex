import path from 'path';
import os from 'os';

// Resolve ~/exocortex-data
export const USER_HOME = os.homedir();
export const EXOCORTEX_DATA_DIR = path.join(USER_HOME, 'exocortex-data');

export const DATA_PATHS = {
  career: path.join(EXOCORTEX_DATA_DIR, 'job-analyzer'),
  analyses: path.join(EXOCORTEX_DATA_DIR, 'job-analyzer/jobs/analyzed'),
  companies: path.join(EXOCORTEX_DATA_DIR, 'job-analyzer/companies'),
  readingList: path.join(EXOCORTEX_DATA_DIR, 'reading-list'),
  recipes: path.join(EXOCORTEX_DATA_DIR, 'recipe-manager/recipes'),
};
