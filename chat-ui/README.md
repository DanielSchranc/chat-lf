This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

1. Install npm packages:

```bash
pnpm install
```

2. Start server (.env has to use your OPENAI api key):

```bash
cd chat-service
docker compose up -d
```

3. Setup env variables (the one for localhost:8000 is shared in example):

```bash
cp .env.example .env.local
```

4. Start UI

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
