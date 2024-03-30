import React from "react";

const TimeAgo = ({ timestamp }: { timestamp: string }) => {
  const timeDifference = new Date().getTime() - new Date(timestamp).getTime();

  const minutes = Math.floor(timeDifference / (1000 * 60));
  const hours = Math.floor(timeDifference / (1000 * 60 * 60));
  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
  const months = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 30));
  const years = Math.floor(timeDifference / (1000 * 60 * 60 * 24 * 365));

  let timeAgo;
  if (years > 0) {
    timeAgo = `${years} year${years > 1 ? "s" : ""} ago`;
  } else if (months > 0) {
    timeAgo = `${months} month${months > 1 ? "s" : ""} ago`;
  } else if (days > 0) {
    timeAgo = `${days} day${days > 1 ? "s" : ""} ago`;
  } else if (hours > 0) {
    timeAgo = `${hours} hour${hours > 1 ? "s" : ""} ago`;
  } else {
    timeAgo = `${minutes} minute${minutes > 1 ? "s" : ""} ago`;
  }

  return <p className="text-xs">{timeAgo}</p>;
};

export default TimeAgo;
