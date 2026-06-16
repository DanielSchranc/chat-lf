import { type NextRequest } from "next/server";

const SERVICE_URL = process.env.CHAT_SERVICE_URL ?? "http://localhost:8000";

async function proxy(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params;
  const url = `${SERVICE_URL}/api/v1/${path.join("/")}${req.nextUrl.search}`;
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
