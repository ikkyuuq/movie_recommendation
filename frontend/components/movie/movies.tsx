"use client";

import { useHorizontalScroll } from "@/hooks";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from "@nextui-org/react";
import Category from "@/components/movie/category";
import Header from "../Header";

export default function Movies({ data }: { data: { results: IMovie[] } }) {
  useEffect(() => {
    const getMoviesData = async () => {
      try {
        setMovies(data.results);
      } catch (error) {
        console.error(error);
      }
    };
    getMoviesData();
  }, [data]);

  const elRef = useHorizontalScroll();
  const [searchContent, setSearchContent] = useState("");
  const [movies, setMovies] = useState<IMovie[]>([]);
  const [genreSelect, setGenreSelect] = useState("Trending");
  const [optionalFilter, setOptionalFilter] = useState("");
  const [sortedMovies, setSortedMovies] = useState<IMovie[]>([
    {
      actors: [],
      directors: [],
      writers: [],
      genres: [],
      id: 0,
      img_url: "",
      overview: "",
      popular: 0,
      rating: 0,
      release_date: new Date(),
      title: "",
      trailer: [],
    },
  ]);

  useEffect(() => {
    const filterMoviesByGenre = () => {
      if (!movies) return;
      if (genreSelect === "Trending") {
        setOptionalFilter("trending");
        setSortedMovies(movies.sort((a, b) => b.popular - a.popular));
      } else {
        const filtered = movies.filter((movie) =>
          movie.genres?.some(
            (genre) =>
              genre.title &&
              genre.title.toLowerCase().includes(genreSelect.toLowerCase())
          )
        );
        setSortedMovies(filtered);
      }
    };
    filterMoviesByGenre();
  }, [genreSelect, ...movies]);

  useEffect(() => {
    let filteredAndSortedMovies = [...movies];

    if (searchContent !== "") {
      filteredAndSortedMovies = movies.filter((movie) =>
        movie.title.toLowerCase().includes(searchContent.toLowerCase())
      );
      setGenreSelect("Trending");
    } else {
      setSortedMovies(movies.slice());
    }

    if (optionalFilter === "name") {
      filteredAndSortedMovies.sort((a, b) => a.title.localeCompare(b.title));
    } else if (optionalFilter === "trending") {
      filteredAndSortedMovies.sort((a, b) => b.popular - a.popular);
    } else if (optionalFilter === "rating") {
      filteredAndSortedMovies.sort((a, b) => b.rating - a.rating);
    } else if (optionalFilter === "release date") {
      filteredAndSortedMovies.sort(
        (a, b) =>
          new Date(b.release_date).getTime() -
          new Date(a.release_date).getTime()
      );
    }

    setSortedMovies(filteredAndSortedMovies);
  }, [optionalFilter, searchContent, movies]);

  return (
    <main className="h-screen flex justify-center items-center bg-[url('/bg-img.jpg')] bg-cover">
      <div className="xl:flex xl:justify-center w-full md:px-10 sm: px-5">
        <div className="flex flex-col gap-10 max-w-7xl bg-slate-200/30 p-10 rounded-3xl backdrop-blur-lg">
          <Header setSearchContent={setSearchContent} />
          <Category setGenreSelect={setGenreSelect} />
          <div className="flex flex-col gap-4">
            <div className="flex items-start justify-between">
              <article className="text-white">
                <h1 className="text-2xl font-medium">
                  {genreSelect && searchContent === ""
                    ? optionalFilter === "trending"
                      ? `Trending in this time`
                      : optionalFilter === "name"
                      ? genreSelect !== "Trending"
                        ? `A-Z in ${genreSelect}`
                        : "A-Z"
                      : optionalFilter === "rating"
                      ? genreSelect !== "Trending"
                        ? `Most rating in ${genreSelect}`
                        : `Most rating in this time`
                      : optionalFilter === "release date"
                      ? genreSelect !== "Trending"
                        ? `Recently released in ${genreSelect}`
                        : "Recently released"
                      : ""
                    : searchContent !== ""
                    ? optionalFilter === "trending"
                      ? `Trending in ${searchContent}`
                      : optionalFilter === "name"
                      ? `A-Z in ${searchContent}`
                      : optionalFilter === "rating"
                      ? `Most rating in ${searchContent}`
                      : optionalFilter === "release date"
                      ? "Recently released"
                      : ""
                    : optionalFilter === "trending"
                    ? "Trending in this time"
                    : optionalFilter === "name"
                    ? "A-Z"
                    : optionalFilter === "genre"
                    ? `Trending in ${genreSelect}`
                    : "Most rating in this time"}
                </h1>
              </article>
              <Dropdown>
                <DropdownTrigger>
                  <div className="flex bg-slate-950 text-white rounded-3xl px-4 py-2">
                    <div className="flex gap-2">
                      <span className="ion--filter"></span>
                      <span className="text-xs capitalize">
                        {optionalFilter}
                      </span>
                    </div>
                    <div className="border-l mx-2 mr-4"></div>
                    <button className="mingcute--filter-line"></button>
                  </div>
                </DropdownTrigger>
                <DropdownMenu
                  className="bg-slate-950 text-white p-3 rounded-2xl text-sm"
                  closeOnSelect={false}
                  selectionMode="single"
                  selectedKeys={optionalFilter}
                  onAction={(key: any) => setOptionalFilter(key)}
                >
                  <DropdownItem
                    className="rounded-lg py-1"
                    key="name"
                    startContent={
                      <span className="icons8--alphabetical-sorting"></span>
                    }
                  >
                    Name
                  </DropdownItem>
                  <DropdownItem
                    className="rounded-lg py-1"
                    key="trending"
                    startContent={
                      <span className="fluent--arrow-trending-lines-24-regular"></span>
                    }
                  >
                    Trending
                  </DropdownItem>
                  <DropdownItem
                    className="rounded-lg py-1"
                    key="rating"
                    startContent={
                      <span className="material-symbols--star"></span>
                    }
                  >
                    Rating
                  </DropdownItem>
                  <DropdownItem
                    className="rounded-lg py-1"
                    key="release date"
                    startContent={
                      <span className="lets-icons--date-fill"></span>
                    }
                  >
                    Release Date
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </div>
            <div
              ref={elRef}
              className="flex gap-4 scroll-pl-10 snap-x scroll-smooth overflow-x-scroll mx-[-40px] px-[40px] min-h-[325px]"
              style={{
                mask: `linear-gradient(90deg, transparent, rgba(255, 255, 255, 1) 5%, rgba(255, 255, 255, 1) 95%, transparent)`,
              }}
            >
              {sortedMovies.map((movie, index) => (
                <Link key={index} href={`/movie/${movie.id}`}>
                  <div
                    className={`${
                      movies.length <= 1 ? "animate-pulse" : ""
                    } snap-start flex rounded-3xl border border-zinc-400/30 justify-start items-end flex-shrink-0`}
                    style={{
                      backgroundImage: `linear-gradient(180deg, rgba(0, 0, 0, 0.00) 45%, rgba(0, 0, 0, 0.40) 75%), url(${movie.img_url})`,
                      backgroundSize: "cover",
                      minHeight: "325px",
                      minWidth: "225px",
                      scrollSnapAlign: "start",
                    }}
                  >
                    <article className="p-5 space-y-2">
                      <h2 className="line-clamp-2 text-base font-bold text-white">
                        {movie.title}
                      </h2>
                      <span className="line-clamp-1 text-xs font-light text-white">
                        <div className="flex content-center items-baseline gap-1">
                          <span className="twemoji--star text-xs"></span>
                          <span className="text-xs">
                            {movie.rating ? movie.rating.toFixed(1) : 0.0}
                          </span>
                          {" | "}
                          {new Date(movie.release_date).toDateString()}
                        </div>
                      </span>
                    </article>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
