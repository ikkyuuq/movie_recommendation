import { useRouter } from "next/router";

const useCurrentRoute = () => {
  const router = useRouter();
  const currentRoute = router.pathname;

  return currentRoute;
};

export default useCurrentRoute;
