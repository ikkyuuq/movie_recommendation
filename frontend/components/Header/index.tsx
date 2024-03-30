import React from "react";
import Navbar from "../Navbar";
import { UserButton, useUser } from "@clerk/nextjs";
import Link from "next/link";
import { Button } from "../ui/button";
import { usePathname } from "next/navigation";

import { Lobster_Two } from "next/font/google";

const logo = Lobster_Two({ subsets: ["latin"], weight: ["400", "700"] });

export default function index({ setSearchContent }) {
  const { isSignedIn, user } = useUser();
  const currentRoute = usePathname();
  return (
    <div className="flex justify-center items-center *:flex-1">
      <div className={`${logo.className} text-white font-bold text-3xl`}>
        Mlynx
      </div>
      <Navbar setSearchContent={setSearchContent} />
      <div className="text-white">
        {isSignedIn ? (
          <div className="flex gap-x-2 items-center justify-end">
            <UserButton />
            <div>
              <h1>
                {user.firstName
                  ?.concat(" ")
                  ?.concat(user.lastName?.substring(0, 4))}
              </h1>
            </div>
          </div>
        ) : (
          <div className="flex gap-x-2 justify-end">
            <Button variant="link" className="text-white">
              <Link href={`/sign-in?redirect_url=${currentRoute}`}>
                🔐Sign in
              </Link>
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
