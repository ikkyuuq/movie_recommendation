"use client";

import DisneyPlus from "@/app/assets/DisneyPlus";
import Hub from "@/app/assets/Hub";
import MyList from "@/app/assets/MyList";
import Netflix from "@/app/assets/Netflix";
import Search from "@/app/assets/Search";
import React, { useState } from "react";

export default function index({
  setSearchContent,
  searchDisable = false,
}: {
  setSearchContent?: React.Dispatch<React.SetStateAction<string>>;
  searchDisable?: boolean;
}) {
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
      href: "/mylist",
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
      svg: <DisneyPlus />,
      href: "/disneyplus",
      status: "disabled",
    },
  ];

  const [search, setSearch] = useState(false);
  return (
    <div className="flex bg-slate-950 p-2 rounded-full mx-auto">
      <ul className="flex items-center gap-1 text-white text-base min-w-[500px]">
        {search ? (
          <input
            onChange={(e) =>
              setSearchContent && setSearchContent(e.target.value)
            }
            type="text"
            placeholder="Search for movies..."
            className="flex py-1 px-5 rounded-full bg-slate-500 text-white placeholder-white/70"
            style={{
              width: search ? "100%" : "0",
              display: search ? "block" : "none",
              transition: "width 0.3s ease-in-out",
              overflow: "hidden",
            }}
          />
        ) : (
          navItems.map((value, index) => (
            <li
              key={index}
              className="py-1 px-5 rounded-full mx-auto"
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
          ))
        )}

        <div className="flex gap-1 h-full">
          <span className="border border-y h-full opacity-30"></span>
          <button
            disabled={searchDisable}
            onClick={() => {
              setSearch((prevState) => !prevState);
            }}
            className="flex justify-center items-center h-[32px] w-[32px] bg-white/30 p-1 rounded-full"
          >
            <Search />
          </button>
        </div>
      </ul>
    </div>
  );
}
