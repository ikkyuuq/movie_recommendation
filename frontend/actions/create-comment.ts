"use server";

import * as z from "zod";

import { CommentSchema } from "@/schemas";

export const createComment = (values: z.infer<typeof CommentSchema>) => {
  const validField = CommentSchema.safeParse(values);

  if (!validField.success) {
    return { error: "Something went wrong!", success: "" };
  }

  return { success: "Comment created!", error: "" };
};
