"use client";

import { iGenres } from "@/app/assets/iGenres";
import { useHorizontalScroll } from "@/hooks";
import React, { useState } from "react";

interface ICategory {
  setGenreSelect: any;
}

interface GenreObject {
  [key: string]: string | undefined;
}

const genresList = [
  "Action",
  "Animation",
  "Adventure",
  "Comedy",
  "Crime",
  "Documentary",
  "Drama",
  "Family",
  "Fantasy",
  "History",
  "Horror",
  "Music",
  "Mystery",
  "Romance",
  "Science Fiction",
  "Thriller",
  "TV Movie",
  "War",
  "Western",
];

function Category({ setGenreSelect }: ICategory) {
  const [genreActive, setGenreActive] = useState("Trending");
  const ref = useHorizontalScroll();

  return (
    <div
      ref={ref}
      className="flex gap-4 scroll-smooth overflow-x-scroll h-full items-center mx-[-40px] px-[40px]"
      style={{
        mask: `linear-gradient(90deg, transparent, rgba(255, 255, 255, 1) 5%, rgba(255, 255, 255, 1) 95%, transparent)`,
      }}
    >
      <div
        className={`px-7 py-5 bg-slate-100/30 text-white rounded-2xl ${
          genreActive === "Trending"
            ? "border-[0.5px] border-slate-200/30 drop-shadow-glow"
            : ""
        }`}
        onClick={() => {
          setGenreActive("Trending");
          setGenreSelect("Trending");
        }}
      >
        <button className="snap-start flex items-center gap-1">
          <span className="mdi--fire text-2xl"></span>
          <h1 className="text-base">Trending</h1>
        </button>
      </div>
      {genresList.map((genre) => {
        const genreObject: GenreObject | undefined = iGenres.find((iGenre) =>
          iGenre.hasOwnProperty(genre)
        );
        return (
          <div
            key={genre}
            className={`px-7 py-5 bg-slate-200/30 text-white rounded-2xl ${
              genreActive === genre
                ? "border-[0.5px] border-slate-200/30 drop-shadow-glow"
                : ""
            }`}
            onClick={() => {
              setGenreActive(genre);
              setGenreSelect(genre);
            }}
          >
            <button className="snap-start flex items-center gap-1">
              <span className={`${genreObject?.[genre]} text-2xl`}></span>
              <h1 className="text-base whitespace-nowrap">{genre}</h1>
            </button>
          </div>
        );
      })}
    </div>
  );
}

export default Category;
