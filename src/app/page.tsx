import { Chat } from "@/components/chat";

export default function Home() {
  return (
    <div className="container mx-auto flex h-full flex-1 flex-col items-center justify-center p-4 md:p-8">
      <Chat />
    </div>
  );
}
