"use client";

import React, { Suspense, useCallback, useEffect, useState } from "react";
import Header from "@/components/Header";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { useUser } from "@clerk/nextjs";
import Loading from "./loading";

function MyListPage() {
  const [lists, setLists] = useState<IList[]>([]);
  const { user } = useUser();

  const fetchLists = useCallback(async () => {
    const url = `${process.env.FAVOUR_URL}?user_id=${user?.id}`;
    const res = await fetch(url);
    const data = await res.json();
    setLists(data.favour);
  }, [lists]);

  useEffect(() => {
    if (user) {
      fetchLists();
    }
  }, [user]);

  const onDelete = (favour_id: number) => {
    const url = `${process.env.FAVOUR_URL}?favour_id=${favour_id}`;
    fetch(url, {
      method: "DELETE",
    }).then((res) => {
      if (res.ok) {
        const newLists = lists.filter((list) => list.favour_id !== favour_id);
        setLists(newLists);
      }
    });
  };

  return (
    <main className="h-screen flex justify-center items-center bg-[url('/bg-img.jpg')] bg-cover">
      <div className="xl:flex xl:justify-center w-full md:px-10 sm:px-5">
        <div className="flex flex-col gap-10 max-w-7xl bg-slate-200/30 p-10 rounded-3xl backdrop-blur-lg">
          <Header searchDisable={true} />
          <div className="bg-white rounded-xl overflow-hidden">
            <table className="table-fixed w-full">
              <thead>
                <tr className="*:border *:py-3">
                  <th>ID</th>
                  <th>Title</th>
                  <th>Release Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody className="overflow-y-scroll">
                {lists == undefined || lists.length == 0 ? (
                  <tr>
                    <td colSpan={4} className="text-center py-6">
                      <div className="space-y-2">
                        <p>Your favorite list is empty!</p>
                        <Button variant="default">
                          <Link href="/">Add New</Link>
                        </Button>
                      </div>
                    </td>
                  </tr>
                ) : (
                  lists &&
                  lists.map((list) => (
                    <tr
                      key={list.favour_id}
                      className="text-center *:border *:py-2"
                    >
                      <td>{list.movie_id}</td>
                      <td>{list.movie_title}</td>
                      <td>
                        {new Date(list.movie_release_date).toDateString()}
                      </td>
                      <td className="space-x-2">
                        <Link href={`/movie/${list.movie_id}`}>
                          <Button variant="default">View</Button>
                        </Link>
                        <Button
                          variant="destructive"
                          onClick={() => onDelete(list.favour_id)}
                        >
                          Delete
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}

export default MyListPage;
