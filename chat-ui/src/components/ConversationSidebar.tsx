"use client";

import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";

type Conversation = { id: string; title: string | null; updated_at: string };

interface ConversationSidebarProps {
  selectedId: string | null;
  onSelect: (id: string | null) => void;
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

  const deleteConversation = async (id: string) => {
    await fetch(`/api/backend/conversations/${id}`, { method: "DELETE" });
    if (selectedId === id) onSelect(null);
    await load();
  };

  return (
    <aside className="w-64 border-r flex flex-col h-full">
      <div className="p-3 border-b">
        <Button variant="outline" className="w-full" onClick={createNew}>
          + New conversation
        </Button>
      </div>
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
          {conversations.map((c) => (
            <div key={c.id} className="group flex items-center gap-1">
              <Button
                variant={c.id === selectedId ? "secondary" : "ghost"}
                className="flex-1 justify-start truncate"
                onClick={() => onSelect(c.id)}
              >
                {c.title ?? "New conversation"}
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="shrink-0 opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive"
                onClick={() => deleteConversation(c.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      </ScrollArea>
    </aside>
  );
}
