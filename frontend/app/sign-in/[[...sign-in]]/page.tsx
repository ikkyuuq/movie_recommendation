import { SignIn } from "@clerk/nextjs";
import React from "react";

function SignInPage() {
  return (
    <div className="h-screen flex justify-center items-center bg-[url('/bg-img.jpg')] bg-cover">
      <SignIn />
    </div>
  );
}

export default SignInPage;
