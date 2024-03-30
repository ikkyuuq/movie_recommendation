export async function getComments(movie_id: number) {
  const url = `${process.env.COMMENT_URL}?movie_id=${movie_id}`;
  const res = await fetch(url);
  const data = await res.json();
  return data;
}
