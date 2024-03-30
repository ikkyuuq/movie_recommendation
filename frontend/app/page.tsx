"use client";

import { useEffect, useState } from "react";
import Movies from "@/components/movie/movies";
import Loading from "./loading";

async function getMovies() {
  const res = await fetch(`${process.env.MOVIE_URL}`);
  const data = await res.json();
  return data;
}

async function updateDatabase() {
  try {
    const url = `${process.env.UPDATEDB_URL}?start_p=1&stop_p=20`;
    const res = await fetch(url);
    if (res.ok) {
      console.log("updated database!");
    }
  } catch (err) {
    console.log(err);
  }
}

export default function Home() {
  const [moviesData, setMoviesData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getMovies();
      setMoviesData(data);
    };

    fetchData();

    const updateInterval = setInterval(() => {
      updateDatabase();
    }, 6 * 60 * 60 * 1000); // 6 hours

    return () => clearInterval(updateInterval);
  }, []);

  return <div>{moviesData ? <Movies data={moviesData} /> : <Loading />}</div>;
}
