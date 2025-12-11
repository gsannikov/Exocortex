import { getIdeas } from '../../lib/api';
import IdeasBoard from './IdeasBoard';

export default async function IdeasPage() {
  const ideas = await getIdeas();
  return <IdeasBoard ideas={ideas} />;
}
