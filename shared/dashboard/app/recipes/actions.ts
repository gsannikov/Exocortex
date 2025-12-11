'use server';

import fs from 'fs/promises';
import path from 'path';
import yaml from 'yaml';
import { revalidatePath } from 'next/cache';
import { DATA_PATHS } from '../../lib/paths';

function statusToFolder(status: string) {
  return status.trim().toLowerCase().replace(/\s+/g, '-');
}

export async function updateRecipeStatus(filePath: string, newStatus: string) {
  try {
    const resolvedPath = path.resolve(filePath);
    const recipesRoot = path.resolve(DATA_PATHS.recipes);

    if (!resolvedPath.startsWith(recipesRoot)) {
      throw new Error('Recipe path outside data directory');
    }

    const content = await fs.readFile(resolvedPath, 'utf-8');
    const data = yaml.parse(content) || {};
    data.status = newStatus;

    const updatedYaml = yaml.stringify(data);

    // Keep files organized by status folder (e.g., to-try, perfected)
    const targetDir = path.join(recipesRoot, statusToFolder(newStatus));
    await fs.mkdir(targetDir, { recursive: true });
    const targetPath = path.join(targetDir, path.basename(resolvedPath));

    if (targetPath !== resolvedPath) {
      await fs.writeFile(targetPath, updatedYaml, 'utf-8');
      await fs.unlink(resolvedPath);
    } else {
      await fs.writeFile(resolvedPath, updatedYaml, 'utf-8');
    }

    const recipeId = path.basename(targetPath, '.yaml');
    revalidatePath('/recipes');
    revalidatePath(`/recipes/${recipeId}`);

    return { success: true, filePath: targetPath };
  } catch (error) {
    console.error('Failed to update recipe status:', error);
    return { success: false, error: 'Failed to update recipe status' };
  }
}

export async function updateRecipeTags(filePath: string, tags: string[]) {
  try {
    const resolvedPath = path.resolve(filePath);
    const recipesRoot = path.resolve(DATA_PATHS.recipes);

    if (!resolvedPath.startsWith(recipesRoot)) {
      throw new Error('Recipe path outside data directory');
    }

    const content = await fs.readFile(resolvedPath, 'utf-8');
    const data = yaml.parse(content) || {};

    // Normalize tags: trim, dedupe, drop empties
    const normalized = Array.from(
      new Set(tags.map((t) => t.trim()).filter(Boolean))
    );

    data.tags = normalized;

    const updatedYaml = yaml.stringify(data);
    await fs.writeFile(resolvedPath, updatedYaml, 'utf-8');

    const recipeId = path.basename(resolvedPath, '.yaml');
    revalidatePath('/recipes');
    revalidatePath(`/recipes/${recipeId}`);

    return { success: true, tags: normalized };
  } catch (error) {
    console.error('Failed to update recipe tags:', error);
    return { success: false, error: 'Failed to update recipe tags' };
  }
}
