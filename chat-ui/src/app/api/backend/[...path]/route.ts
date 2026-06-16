import { type NextRequest } from "next/server";

const API_URL = process.env.CHAT_API_URL ?? "";

if (!API_URL) {
  throw new Error("CHAT_API_URL env variable is not set");
}

async function proxy(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  const url = `${API_URL}/api/v1/${path.join("/")}${req.nextUrl.search}`;
  const res = await fetch(url, {
    method: req.method,
    headers: { "Content-Type": "application/json" },
    body: req.method !== "GET" ? req.body : undefined,
    // @ts-expect-error duplex required for streaming request body
    duplex: "half",
  });

  return new Response(res.body, {
    status: res.status,
    headers: {
      "Content-Type": res.headers.get("Content-Type") ?? "application/json",
      "Cache-Control": "no-cache",
      "X-Accel-Buffering": "no",
    },
  });
}

export const GET = proxy;
export const POST = proxy;
export const DELETE = proxy;
