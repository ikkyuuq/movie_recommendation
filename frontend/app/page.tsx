"use client";
import DsineyPlus from "./assets/DsineyPlus";
import Hub from "./assets/Hub";
import MyList from "./assets/MyList";
import Netflix from "./assets/Netflix";
import Search from "./assets/Search";
import { useHorizontalScroll } from "./hooks";

export default function Home() {
  const movies = [
    {
      movie_name: "The Mavels",
      movie_release: 2023,
      movie_rating: 6.8,
      movie_genres: ["Action", "Adventure", "Sci-fi"],
      movie_poster:
        "https://image.tmdb.org/t/p/original/9GBhzXMFjgcZ3FdR9w3bUMMTps5.jpg",
    },
    {
      movie_name: "Lift",
      movie_release: 2024,
      movie_rating: 6.8,
      movie_genres: ["Comedy", "Crime"],
      movie_poster:
        "https://image.tmdb.org/t/p/original/gma8o1jWa6m0K1iJ9TzHIiFyTtI.jpg",
    },
    {
      movie_name: "Wonka",
      movie_release: 2023,
      movie_rating: 7.2,
      movie_genres: ["Comedy", "Fantasy", "Family"],
      movie_poster:
        "https://image.tmdb.org/t/p/original/qhb1qOilapbapxWQn9jtRCMwXJF.jpg",
    },
    {
      movie_name: "Wonka",
      movie_release: 2023,
      movie_rating: 7.2,
      movie_genres: ["Comedy", "Fantasy", "Family"],
      movie_poster:
        "https://image.tmdb.org/t/p/original/qhb1qOilapbapxWQn9jtRCMwXJF.jpg",
    },
    {
      movie_name: "Wonka",
      movie_release: 2023,
      movie_rating: 7.2,
      movie_genres: ["Comedy", "Fantasy", "Family"],
      movie_poster:
        "https://image.tmdb.org/t/p/original/qhb1qOilapbapxWQn9jtRCMwXJF.jpg",
    },
    {
      movie_name: "Wonka",
      movie_release: 2023,
      movie_rating: 7.2,
      movie_genres: ["Comedy", "Fantasy", "Family"],
      movie_poster:
        "https://image.tmdb.org/t/p/original/qhb1qOilapbapxWQn9jtRCMwXJF.jpg",
    },
  ];
  const navItems = [
    {
      text: "All+",
      svg: <Hub />,
      href: "/",
      status: "enabled",
    },
    {
      text: "My Lists",
      svg: <MyList />,
      href: "/mylists",
      status: "enabled",
    },
    {
      text: "Netflix",
      svg: <Netflix />,
      href: "/netflix",
      status: "disabled",
    },
    {
      text: "Disney+",
      svg: <DsineyPlus />,
      href: "/disneyplus",
      status: "disabled",
    },
  ];

  const elRef = useHorizontalScroll();
  return (
    <main className="h-screen w-screen flex flex-col justify-center items-center bg-[url('https://images.unsplash.com/photo-1682687220067-dced9a881b56?q=80&w=1975&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')]">
      <div className="flex flex-col w-3/4 justify-center items-center gap-4">
        {/* Movies Container */}
        <div className="flex flex-col gap-4 max-w-5xl w-full bg-zinc-400/30 px-10 py-5 rounded-3xl border-zinc-400 border backdrop-blur-sm">
          <div className="flex items-start justify-between">
            <article className="text-white">
              <h1>Welcome back, Guest!</h1>
              <p>We have ranked all of the popular movies at this time.</p>
            </article>
            <button className="flex bg-black/25 px-8 py-2 rounded-full text-white">
              Switch View
            </button>
          </div>

          <div
            ref={elRef}
            className="flex gap-4 scroll-pl-10 snap-x scroll-smooth overflow-x-scroll mx-[-40px] px-[40px]"
          >
            {movies.map((value, index) => {
              const styles = {
                backgroundImage: `linear-gradient(180deg, rgba(0, 0, 0, 0.00) 45%, rgba(0, 0, 0, 0.40) 75%), url(${value.movie_poster})`,
                backgroundSize: "cover",
                minHeight: "325px",
                minWidth: "225px",
              };
              return (
                <div
                  key={index}
                  className="snap-start flex rounded-3xl justify-start items-end"
                  style={styles}
                >
                  <article className="p-5 text-white">
                    <span>
                      {value.movie_rating} <span>/ 10</span>
                    </span>
                    <h2>{value.movie_name}</h2>
                    <span>
                      {value.movie_release} -{" "}
                      {value.movie_genres
                        .map((value, index) => value)
                        .join(", ")}
                    </span>
                  </article>
                </div>
              );
            })}
          </div>
        </div>
        {/* Movies Container */}
        {/* Navbar */}
        <div className="flex bg-zinc-400/30 p-1 rounded-full border-zinc-400 border ">
          <ul className="flex items-center gap-1 text-white">
            {navItems.map((value, index) => (
              <li
                key={index}
                className="py-1 px-5 rounded-full"
                style={{
                  opacity: value.status === "disabled" ? 0.5 : 1,
                  pointerEvents: value.status === "disabled" ? "none" : "all",
                }}
              >
                <a href={value.href} className="flex gap-1 items-center">
                  {value.svg}
                  {value.text}
                </a>
              </li>
            ))}
            <div className="flex gap-1 h-full">
              <span className="border border-y h-full opacity-30"></span>
              <button className="flex justify-center items-center h-[32px] w-[32px] bg-white/30 p-1 rounded-full">
                <Search />
              </button>
            </div>
          </ul>
        </div>
        {/* Navbar */}
      </div>
    </main>
  );
}
