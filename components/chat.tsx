"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { Bot, Send, User } from "lucide-react";
import { useEffect, useRef, useState, useTransition } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { getBotResponse } from "@/app/actions";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";

const formSchema = z.object({
  message: z.string().min(1, { message: "Message cannot be empty." }),
});

type Message = {
  role: "user" | "bot";
  content: string;
};

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isPending, startTransition] = useTransition();
  const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      message: "",
    },
  });

  const viewport = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (viewport.current) {
      viewport.current.scrollTop = viewport.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isPending]);

  const onSubmit = (values: z.infer<typeof formSchema>) => {
    const userMessage: Message = { role: "user", content: values.message };
    setMessages((prev) => [...prev, userMessage]);
    form.reset();

    startTransition(async () => {
      const botResponse = await getBotResponse(values.message);
      if (!botResponse) {
        toast({
          variant: "destructive",
          title: "An error occurred",
          description: "Failed to get a response from the bot.",
        });
        setMessages((prev) =>
          prev.slice(0, prev.length -1)
        );
        return;
      }
      const botMessage: Message = { role: "bot", content: botResponse };
      setMessages((prev) => [...prev, botMessage]);
    });
  };

  return (
    <Card className="w-full max-w-2xl h-[calc(100vh-10rem)] flex flex-col mx-auto shadow-2xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-3 text-2xl font-bold tracking-tight">
          <Bot className="h-7 w-7" />
          <span className="font-headline">MEMORA</span>
        </CardTitle>
        <CardDescription>
          A minimalist chatbot with dynamic responses.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden">
        <ScrollArea className="h-full" viewportRef={viewport}>
          <div className="px-4 space-y-6">
            {messages.map((message, index) => (
              <div
                key={index}
                className={cn(
                  "flex items-end gap-3 animate-in fade-in slide-in-from-bottom-2 duration-300",
                  message.role === "user" ? "justify-end" : "justify-start"
                )}
              >
                {message.role === "bot" && (
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-accent">
                      <Bot className="h-5 w-5 text-accent-foreground" />
                    </AvatarFallback>
                  </Avatar>
                )}
                <div
                  className={cn(
                    "max-w-[75%] rounded-2xl px-4 py-3 text-sm shadow-md",
                    message.role === "user"
                      ? "bg-primary text-primary-foreground rounded-br-none"
                      : "bg-card border rounded-bl-none"
                  )}
                >
                  {message.content}
                </div>
                {message.role === "user" && (
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      <User className="h-5 w-5" />
                    </AvatarFallback>
                  </Avatar>
                )}
              </div>
            ))}
            {isPending && (
              <div className="flex items-end gap-3 justify-start animate-in fade-in slide-in-from-bottom-2 duration-300">
                <Avatar className="h-8 w-8">
                  <AvatarFallback className="bg-accent">
                    <Bot className="h-5 w-5 text-accent-foreground" />
                  </AvatarFallback>
                </Avatar>
                <div className="bg-card border rounded-2xl rounded-bl-none px-4 py-3 shadow-md">
                  <div className="flex items-center justify-center gap-1.5">
                    <span className="h-2 w-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                    <span className="h-2 w-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                    <span className="h-2 w-2 bg-muted-foreground rounded-full animate-bounce"></span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
      <CardFooter className="border-t pt-6">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="flex w-full items-center gap-3"
          >
            <FormField
              control={form.control}
              name="message"
              render={({ field }) => (
                <FormItem className="flex-1">
                  <FormControl>
                    <Input
                      placeholder="Ask me anything..."
                      {...field}
                      autoComplete="off"
                      disabled={isPending}
                    />
                  </FormControl>
                </FormItem>
              )}
            />
            <Button type="submit" size="icon" disabled={isPending}>
              <Send className="h-5 w-5" />
              <span className="sr-only">Send message</span>
            </Button>
          </form>
        </Form>
      </CardFooter>
    </Card>
  );
}
