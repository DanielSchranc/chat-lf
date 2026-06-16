"use client";

import { fetchEventSource } from "@microsoft/fetch-event-source";
import { useCallback, useState } from "react";

export type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export function useChatStream(conversationId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const loadHistory = useCallback(async (conId: string) => {
    const res = await fetch(`/api/backend/conversations/${conId}/messages`);
    const data: ChatMessage[] = await res.json();
    setMessages(data.map((m) => ({ id: m.id, role: m.role, content: m.content })));
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "user", content },
      ]);
      setIsStreaming(true);

      let buffer = "";
      const assistantId = crypto.randomUUID();

      await fetchEventSource(`/api/backend/conversations/${conversationId}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
        onmessage: (event) => {
          if (event.data === "[DONE]") {
            return;
          }

          const parsed = JSON.parse(event.data) as {
            chunk?: string;
            error?: string;
          };

          if (parsed.error) {
            throw new Error(parsed.error);
          }

          buffer += parsed.chunk ?? "";

          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant") {
              return [
                ...prev.slice(0, -1),
                { id: assistantId, role: "assistant", content: buffer },
              ];
            }
            return [...prev, { id: assistantId, role: "assistant", content: buffer }];
          });
        },
        onerror: (err) => {
          setIsStreaming(false);
          throw err;
        },
        onclose: () => {
          setIsStreaming(false);
        },
      });
      setIsStreaming(false);
    },
    [conversationId],
  );

  return { messages, sendMessage, isStreaming, loadHistory };
}
