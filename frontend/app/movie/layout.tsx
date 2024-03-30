import Header from "@/components/Header";
import React from "react";

function MovieLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="h-full py-10 flex justify-center items-center bg-[url('/bg-img.jpg')] bg-cover">
      <div className="flex flex-col gap-10 max-w-7xl bg-slate-200/30 p-10 rounded-3xl backdrop-blur-lg">
        {children}
      </div>
    </main>
  );
}

export default MovieLayout;
