import React from "react";
import { CheckCircledIcon } from "@radix-ui/react-icons";

interface IFormSuccess {
  message?: string;
}
function FormSuccess({ message }: IFormSuccess) {
  if (!message) return null;
  return (
    <div className="flex p-3 bg-green-500/25 rounded-md items-center gap-x-2 text-green-600 text-sm">
      <CheckCircledIcon className="h-4 w-4" />
      <p>{message}</p>
    </div>
  );
}

export default FormSuccess;
