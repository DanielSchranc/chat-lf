"use client";

import { useEffect, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";

type Conversation = { id: string; title: string | null; updated_at: string };

interface ConversationSidebarProps {
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export function ConversationSidebar({
  selectedId,
  onSelect,
}: ConversationSidebarProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const load = async () => {
    const res = await fetch("/api/backend/conversations");
    setConversations(await res.json());
  };

  useEffect(() => {
    load();
  }, []);

  const createNew = async () => {
    const res = await fetch("/api/backend/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{}",
    });
    const conv = (await res.json()) as { id: string };
    await load();
    onSelect(conv.id);
  };

  return (
    <aside className="w-64 border-r flex flex-col h-full">
      <div className="p-3 border-b">
        <Button
          variant="outline"
          className="w-full"
          onClick={createNew}
        >
          + New conversation
        </Button>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
          {conversations.map((c) => (
            <Button
              key={c.id}
              variant={c.id === selectedId ? "secondary" : "ghost"}
              className="w-full justify-start truncate"
              onClick={() => onSelect(c.id)}
            >
              {c.title ?? "New conversation"}
            </Button>
          ))}
        </div>
      </ScrollArea>
    </aside>
  );
}
