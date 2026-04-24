import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-background">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold text-center mb-8">LegaFlo</h1>
        <p className="text-center mb-12 text-muted-foreground">End-to-end Legal Operating System</p>
        
        <div className="grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-3 lg:text-left gap-4">
          <Link
            href="/citizen"
            className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 dark:hover:border-neutral-700 dark:hover:bg-neutral-800/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Citizen Portal{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                -&gt;
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Public Legal Self-Help, AI Translation, Find an Advocate.
            </p>
          </Link>

          <Link
            href="/advocate"
            className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 dark:hover:border-neutral-700 dark:hover:bg-neutral-800/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Advocate Portal{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                -&gt;
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Solo Practice Command Center, Case Tracking, AI Lawyer Chat.
            </p>
          </Link>

          <Link
            href="/firm"
            className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 dark:hover:border-neutral-700 dark:hover:bg-neutral-800/30"
          >
            <h2 className="mb-3 text-2xl font-semibold">
              Law Firm Portal{" "}
              <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                -&gt;
              </span>
            </h2>
            <p className="m-0 max-w-[30ch] text-sm opacity-50">
              Enterprise Workspace, Team Collaboration, Centralized Billing.
            </p>
          </Link>
        </div>
      </div>
    </main>
  );
}
