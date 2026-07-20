import ChatInterface from "@/components/chat-interface";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <header className="border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground text-sm font-bold">
              FC
            </div>
            <div>
              <h1 className="text-sm font-semibold leading-tight">
                Financial AI Copilot
              </h1>
              <p className="text-xs text-muted-foreground">
                Enterprise Financial Analysis
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-500">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              Connected
            </span>
          </div>
        </div>
      </header>
      <ChatInterface />
    </main>
  );
}
