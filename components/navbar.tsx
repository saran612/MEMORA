import Link from "next/link";
import { Button } from "./ui/button";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 max-w-screen-2xl items-center justify-between px-[50px]">
        <div className="flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2">
            <span className="font-bold">MEMORA</span>
          </Link>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost">Log in</Button>
          <Button>Sign Up</Button>
        </div>
      </div>
    </header>
  );
}
