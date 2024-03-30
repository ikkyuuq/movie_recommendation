import React from "react";

function Loading() {
  return (
    <div className="flex justify-center items-center h-screen bg-[url('/bg-img.jpg')] bg-cover">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white"></div>
    </div>
  );
}

export default Loading;
