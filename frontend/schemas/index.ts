import * as z from "zod";

export const SignUpSchema = z.object({
  displayName: z
    .string()
    .min(1, { message: "Display name must contains 1 or more characters" }),
  username: z
    .string()
    .min(1, { message: "Username must contains 1 or more characters" }),
  email: z.string().email({ message: "Email is required" }),
  password: z
    .string()
    .min(6, { message: "Password must contains 6 or more characters" }),
});

export const SignInSchema = z.object({
  username: z.string().min(1, { message: "Username is required" }),
  password: z.string().min(1, { message: "Password is required" }),
});

export const CommentSchema = z.object({
  content: z.string().min(10, {
    message: "Comment content must contains 10 or more characters",
  }),
});
