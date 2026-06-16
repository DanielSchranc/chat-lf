"use client";

import { Trash2Icon, PlusCircleIcon } from "lucide-react";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

type Conversation = { id: string; title: string | null; updated_at: string };

interface ConversationSidebarProps {
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}

export function ConversationSidebar({ selectedId, onSelect }: ConversationSidebarProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const load = async () => {
    const res = await fetch("/api/backend/conversations");
    setConversations(await res.json());
  };

  useEffect(() => {
    load();
  }, []);

  const createConversation = async () => {
    const date = new Date();
    const dateLocale = date.toLocaleDateString("en-GB", { weekday: "long" });
    const dateLocaleTime = date.toLocaleTimeString("en-GB");

    const conversationTitle = `Conversation from ${dateLocale} at ${dateLocaleTime}`;

    const res = await fetch("/api/backend/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: conversationTitle }),
    });
    const conversation = (await res.json()) as { id: string };
    await load();
    onSelect(conversation.id);
  };

  const deleteConversation = async (id: string) => {
    await fetch(`/api/backend/conversations/${id}`, { method: "DELETE" });
    if (selectedId === id) {
      onSelect(null);
    }
    await load();
  };

  return (
    <aside className="w-72 border-r flex flex-col h-full">
      <div className="p-3 border-b">
        <Button
          variant="outline"
          className="w-full"
          onClick={createConversation}
        >
          <PlusCircleIcon /> New conversation
        </Button>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
          {conversations.map((c) => (
            <div
              key={c.id}
              className="group flex items-center gap-1"
            >
              <Button
                variant={c.id === selectedId ? "secondary" : "ghost"}
                className="flex-1 justify-start truncate"
                onClick={() => onSelect(c.id)}
              >
                {c.title ?? "Conversation"}
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="shrink-0 opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive"
                onClick={() => deleteConversation(c.id)}
              >
                <Trash2Icon className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      </ScrollArea>
    </aside>
  );
}
