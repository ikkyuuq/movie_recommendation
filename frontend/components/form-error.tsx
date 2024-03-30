import React from "react";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";

interface IFormError {
  message?: string;
}
function FormError({ message }: IFormError) {
  if (!message) return null;
  return (
    <div className="flex p-3 bg-red-400/25 rounded-md items-center gap-x-2 text-red-600 text-sm">
      <ExclamationTriangleIcon className="h-4 w-4" />
      <p>{message}</p>
    </div>
  );
}

export default FormError;
