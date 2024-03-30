"use client";

import { useCallback, useEffect, useState } from "react";
import "../_style/index.css";
import Header from "@/components/Header";
import CommentSection from "@/components/movie/comment-section";
import { useUser } from "@clerk/nextjs";
import { getMovie } from "@/api/movie";
const dotenv = require("dotenv");
dotenv.config();

const Movie = ({ params }: { params: { id: number } }) => {
  const [movie, setMovie] = useState<IMovie | undefined>();
  const [lists, setLists] = useState<(number | undefined)[]>([]);

  const { user } = useUser();
  useEffect(() => {
    const fetchLists = async () => {
      try {
        const url = `${process.env.FAVOUR_URL}?user_id=${user?.id}`;
        const listData = await fetch(url);
        const data = await listData.json();
        const movieIds = data.favour.map((list: IList) => list.movie_id);
        setLists(movieIds);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    if (user?.id) {
      fetchLists();
    }
  }, [user?.id]);

  const fetchData = useCallback(async () => {
    try {
      const movieData = await getMovie(params.id);
      setMovie(movieData.results[0]);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }, [params.id]);

  useEffect(() => {
    if (params.id) {
      fetchData();
    }
  }, [params.id]);

  const handleFavourButton = () => {
    const isInList = lists?.includes(movie?.id);
    const url = `${process.env.FAVOUR_URL}`;
    if (isInList) {
      fetch(url, {
        method: "DELETE",
        body: JSON.stringify({
          user_id: user?.id,
          movie_id: movie?.id,
        }),
      }).then(() => {
        setLists((prevLists) => prevLists.filter((id) => id !== movie?.id));
      });
    } else {
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: user?.id,
          movie_id: movie?.id,
          movie_title: movie?.title,
          movie_release_date: new Date(
            movie ? movie.release_date.toString() : ""
          ).toLocaleDateString(),
        }),
      }).then(() => {
        setLists((prevLists) => [...prevLists, movie?.id]);
      });
    }
  };

  return (
    <>
      <Header />
      <div className="flex flex-col gap-4">
        <div className="flex items-start justify-between">
          <article className="text-white">
            <div className="flex gap-3">
              <h1 className="text-2xl font-semibold">
                {movie?.rating ? movie?.rating.toFixed(1) : 0.0}
              </h1>
              <div className="flex items-center border-white/30 border"></div>
              <h1 className="text-2xl font-semibold">{movie?.title}</h1>
            </div>
          </article>
          <button
            onClick={() => handleFavourButton()}
            className="flex bg-black/25 px-8 py-2 rounded-full text-white text-sm"
          >
            {lists?.includes(movie?.id)
              ? "Remove From Favour"
              : "Add To Favour"}
          </button>
        </div>
        <div className="flex gap-10">
          <div
            className="poster flex rounded-3xl border border-zinc-400/30 justify-center items-end p-5"
            style={{
              backgroundImage: `linear-gradient(180deg, rgba(0, 0, 0, 0.00) 70%, rgba(0, 0, 0, 0.40) 75%), url(${movie?.img_url})`,
              backgroundSize: "cover",
              minHeight: "400px",
              maxHeight: "400px",
              minWidth: "275px",
            }}
          ></div>
          <div className="flex flex-col gap-10 w-full">
            <iframe
              className="rounded-2xl w-full h-[400px]"
              src={`https://www.youtube.com/embed/${
                movie?.trailer && movie?.trailer[0].id
              }`}
              allowFullScreen
            ></iframe>
            <div className="flex w-full *:flex-1">
              <article className="text-white">
                <div className="flex flex-1 gap-10">
                  <div className="flex flex-col flex-1 gap-2">
                    <h1 className="font-semibold">Synopsis</h1>
                    <p className="line-clamp-[9]">{movie?.overview}</p>
                  </div>
                  <div className="flex flex-1 *:flex-1 gap-10">
                    <div className="flex flex-col gap-5">
                      <div className="space-y-2">
                        <h1 className="font-semibold">Release Date</h1>
                        <p>
                          {new Date(
                            movie ? movie.release_date : ""
                          ).toDateString()}
                        </p>
                      </div>
                      <div className="space-y-2">
                        <h1 className="font-semibold">Actor</h1>
                        <div>
                          {movie?.actors &&
                            movie.actors
                              .sort((a, b) => b.popular - a.popular)
                              .slice(0, 5)
                              .map((actor) => (
                                <p>
                                  {actor.fname
                                    .concat(" ")
                                    .concat(actor.mname)
                                    .concat(" ")
                                    .concat(actor.lname)}
                                </p>
                              ))}
                          {movie?.actors && movie?.actors.length > 5 && (
                            <p className="font-medium">
                              See more {movie.actors.length - 5}+
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex flex-col col-start-3 gap-5">
                      <div className="space-y-2">
                        <h1 className="font-semibold">Genres</h1>
                        <p>
                          {movie?.genres &&
                            movie?.genres
                              .map((genre) => genre.title)
                              .join(", ")}
                        </p>
                      </div>
                      <div className="space-y-2">
                        <h1 className="font-semibold">Directors</h1>
                        {movie?.directors &&
                          movie.directors.map((director) => (
                            <p>
                              {director.fname
                                .concat(" ")
                                .concat(director.mname)
                                .concat(" ")
                                .concat(director.lname)}
                            </p>
                          ))}
                      </div>
                      <div className="space-y-2">
                        <h1 className="font-semibold">Writers</h1>
                        {movie?.writers &&
                          movie.writers.map((writer) => (
                            <p>
                              {writer.fname
                                .concat(" ")
                                .concat(writer.mname)
                                .concat(" ")
                                .concat(writer.lname)}
                            </p>
                          ))}
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </div>
      </div>
      <CommentSection movieId={movie?.id} />
    </>
  );
};

export default Movie;
