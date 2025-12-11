import { getReadingList } from '../../lib/api';
import ReadingBoard from './ReadingBoard';

export default async function ReadingPage() {
  const readingList = await getReadingList();

  return <ReadingBoard items={readingList} />;
}
