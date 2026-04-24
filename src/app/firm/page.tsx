export default function FirmDashboard() {
  return (
    <div className="grid gap-6">
      <h2 className="text-2xl font-bold tracking-tight">Enterprise Workspace Overview</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Total Firm Cases</h3>
            <p className="text-sm text-muted-foreground">Across all advocates</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">145</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Active Advocates</h3>
            <p className="text-sm text-muted-foreground">Currently logged in</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">8 / 15</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Monthly Revenue</h3>
            <p className="text-sm text-muted-foreground">Collected this month</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">₹ 8.5L</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Conflict Checks</h3>
            <p className="text-sm text-muted-foreground">Last 30 days</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">24</p>
          </div>
        </div>
      </div>
    </div>
  );
}
