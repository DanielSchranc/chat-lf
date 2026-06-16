"use client";

import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

interface ChatComposerProps {
  onSend: (content: string) => void;
  disabled: boolean;
}

export function ChatComposer({ onSend, disabled }: ChatComposerProps) {
  const [value, setValue] = useState("");

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return (
    <div className="border-t p-4">
      <div className="flex gap-2 max-w-2xl mx-auto">
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Type a message… (Enter to send, Shift+Enter for newline)"
          disabled={disabled}
          rows={1}
          className="resize-none"
        />
        <Button onClick={submit} disabled={disabled || !value.trim()}>
          Send
        </Button>
      </div>
    </div>
  );
}
