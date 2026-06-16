"use client";

import { useEffect, useState } from "react";

import { ConversationSidebar } from "@/components/ConversationSidebar";
import { MessageInput } from "@/components/MessageInput";
import { MessageThread } from "@/components/MessageThread";
import { useChatStream } from "@/lib/useChatStream";

export default function Home() {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const { messages, sendMessage, isStreaming, loadHistory } = useChatStream(
    conversationId ?? "",
  );

  useEffect(() => {
    if (conversationId) {
      loadHistory(conversationId);
    }
  }, [conversationId, loadHistory]);

  return (
    <div className="flex h-screen">
      <ConversationSidebar
        selectedId={conversationId}
        onSelect={setConversationId}
      />
      <main className="flex-1 flex flex-col overflow-hidden">
        {conversationId ? (
          <>
            <MessageThread messages={messages} />
            <MessageInput
              onSend={sendMessage}
              disabled={isStreaming}
            />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            Select or create a conversation to start chatting
          </div>
        )}
      </main>
    </div>
  );
}
