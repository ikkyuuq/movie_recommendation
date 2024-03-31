"use client";

import React from "react";
import TimeAgo from "./timeago";
import { Button } from "../ui/button";
import Image from "next/image";

function CommentBox({
  comment,
  likes,
  setLike,
  userId,
}: {
  comment: IComment;
  likes: number[];
  setLike: React.Dispatch<React.SetStateAction<number[]>>;
  userId: string | undefined;
}) {
  const handleLike = () => {
    const isLiked = likes.includes(comment.comment_id);
    const newLikes = isLiked
      ? likes.filter((id) => id !== comment.comment_id)
      : [...likes, comment.comment_id];
    const newAction = isLiked ? "unlike" : "like";
    if (comment.comment_id && userId) {
      fetch(`${process.env.LIKE_URL}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          comment_id: comment.comment_id,
          action: newAction,
          user_id: userId,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to update like");
          }
          setLike(newLikes);
        })
        .catch((error) => {
          console.error("Error updating like:", error);
        });
    } else {
      console.error("No data of comment_id or movie_id");
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-4 border rounded-3xl p-4">
        <div className="flex gap-2 items-center">
          <div className="space-y-2">
            <div className="flex gap-x-2 items-center">
              <Image
                width={40}
                height={40}
                className="rounded-full"
                src={comment.img_url}
                alt="user image"
              />
              <div className="space-y">
                <h1 className="text-slate-950 font-medium">
                  {comment.displayName}
                </h1>
                <TimeAgo timestamp={comment.timestamp} />
              </div>
            </div>
            <p className="text-slate-950">{comment.content}</p>
          </div>
          <span className="icon-[ri--more-fill] text-slate-200/50 text-3xl"></span>
        </div>
        <div className="flex gap-4">
          <Button variant="outline" className="text-xs" onClick={handleLike}>
            ❤️ {likes.includes(comment.comment_id) ? "Unlike" : "Like"}{" "}
            {comment.like_count === 0 ? "" : comment.like_count}
          </Button>
          <Button disabled variant="outline" className="text-xs">
            📃 Reply
          </Button>
        </div>
      </div>
    </div>
  );
}

export default CommentBox;
