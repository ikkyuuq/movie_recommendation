export async function getMovie(id?: number) {
  try {
    let url = `${process.env.MOVIE_URL}`;
    if (id) {
      url += `?tmdb_id=${id}`;
    }
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`Failed to fetch data from ${url}`);
    }
    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Error fetching movie data:", error);
    return null;
  }
}
