"use client";

import React, { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@nextui-org/react";
import Link from "next/link";
import FormError from "@/components/form-error";
import FormSuccess from "@/components/form-success";
import {
  FormField,
  FormItem,
  FormControl,
  FormMessage,
  Form,
} from "../ui/form";
import { createComment } from "@/actions/create-comment";
import { CommentSchema } from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { usePathname } from "next/navigation";
import { z } from "zod";
import { useUser } from "@clerk/nextjs";
import CommentBox from "./comment";
import { useForm } from "react-hook-form";

function CommentSection({ movieId }: { movieId: number }) {
  const [comments, setComments] = useState<IComment[]>([]);
  const [commentsToShow, setCommentsToShow] = useState<number>(5);

  const [pending, setPending] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string>("");
  const [errorMsg, setErrorMsg] = useState<string>("");

  const { isSignedIn, user } = useUser();
  const currentRoute = usePathname();

  const form = useForm<z.infer<typeof CommentSchema>>({
    resolver: zodResolver(CommentSchema),
    defaultValues: {
      content: "",
    },
  });

  const [likes, setLike] = useState<number[]>([]);

  const fetchComments = useCallback(async () => {
    try {
      if (!movieId) return;
      const url = `${process.env.COMMENT_URL}?movie_id=${movieId}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setComments(data.comments);
      } else {
        console.error("Error fetching data:", res.statusText);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }, [movieId, setLike]);

  useEffect(() => {
    if (movieId) {
      fetchComments();
    }
  }, [movieId, likes]);

  const fetchLikes = useCallback(async () => {
    try {
      if (!user?.id && !movieId) return;
      const url = `${process.env.LIKE_URL}?user_id=${user?.id}&movie_id=${movieId}`;
      const res = await fetch(url);
      const data = await res.json();
      const likeIds = data.likes.map((like: IComment) => like.comment_id);
      setLike(likeIds);

      return data;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }, [user?.id, movieId]);

  useEffect(() => {
    if (user?.id && movieId) {
      fetchLikes();
    }
  }, [user?.id, movieId]);

  const onSubmit = async (values: z.infer<typeof CommentSchema>) => {
    setErrorMsg("");
    setSuccessMsg("");
    const url = `http://localhost:5000/comment?movie_id=${movieId}`;
    const displayName = user?.firstName
      ?.concat(" ")
      .concat(user.lastName ? user.lastName : "");
    await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: values.content,
        user_id: user?.id.toString(),
        name: user?.username || displayName,
        img_url: user?.imageUrl,
      }),
    });
    fetchComments();
    const res = await createComment(values);
    setErrorMsg(res.error);
    setSuccessMsg(res.success);
    setPending((prev) => !prev);
    form.reset();
    setTimeout(() => {
      setErrorMsg("");
      setSuccessMsg("");
      setPending((prev) => !prev);
    }, 3000);
  };

  return (
    <div className="flex flex-col gap-4 w-full h-full bg-white rounded-3xl p-5">
      <h1 className=" text-2xl font-semibold p-3">Comments & Reviews</h1>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-8 border shadow-md rounded-3xl p-4"
        >
          <FormField
            control={form.control}
            name="content"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="w-full">
                    <div className="space-y-2">
                      <Textarea
                        disabled={!isSignedIn}
                        className="bg-white rounded-xl border-none"
                        placeholder="Type your comment here."
                        {...field}
                      />
                      <div className="flex justify-between items-center space-x-2">
                        <div className="flex items-center">
                          {isSignedIn ? (
                            <FormMessage />
                          ) : (
                            <Button
                              variant="link"
                              className="text-sm text-red-700"
                            >
                              <Link
                                href={`/sign-in?redirect_url=${currentRoute}`}
                              >
                                🔐 Sign in to leave a comment.
                              </Link>
                            </Button>
                          )}
                        </div>
                        <Button
                          type="submit"
                          disabled={!isSignedIn || pending}
                          className="bg-slate-950"
                        >
                          Submit 📩
                        </Button>
                      </div>
                    </div>
                  </div>
                </FormControl>
              </FormItem>
            )}
          ></FormField>
          <FormSuccess message={successMsg} />
          <FormError message={errorMsg} />
        </form>
      </Form>
      {comments
        .sort(
          (a, b) =>
            b.like_count - a.like_count ||
            new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
        )
        .slice(0, commentsToShow)
        .map((comment, index) => (
          <div key={comment.comment_id}>
            <CommentBox
              comment={comment}
              likes={likes}
              setLike={setLike}
              userId={user?.id}
            />
          </div>
        ))}
      {comments.length > commentsToShow && (
        <Button
          onClick={() => {
            setCommentsToShow((prev) => prev + 3);
          }}
          className="text-sm text-white bg-slate-950"
        >
          Show More
        </Button>
      )}
      {commentsToShow > 5 && (
        <Button
          onClick={() => setCommentsToShow(5)}
          className="text-sm text-white bg-slate-950"
        >
          Show Less
        </Button>
      )}
    </div>
  );
}

export default CommentSection;
