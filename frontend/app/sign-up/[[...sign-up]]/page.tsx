import { SignUp } from "@clerk/nextjs";
import React from "react";

function SignUpPage() {
  return (
    <div className="h-screen flex justify-center items-center bg-[url('/bg-img.jpg')] bg-cover">
      <SignUp />
    </div>
  );
}

export default SignUpPage;
