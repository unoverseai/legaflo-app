export default function CitizenDashboard() {
  return (
    <div className="grid gap-6">
      <h2 className="text-2xl font-bold tracking-tight">Welcome to Public Legal Self-Help</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {/* Placeholder cards for dashboard widgets */}
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Active Cases</h3>
            <p className="text-sm text-muted-foreground">Track your CNR statuses</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">0</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Recent Translations</h3>
            <p className="text-sm text-muted-foreground">Documents translated to regional languages</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-sm text-muted-foreground">No recent documents.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
