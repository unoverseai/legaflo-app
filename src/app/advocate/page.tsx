export default function AdvocateDashboard() {
  return (
    <div className="grid gap-6">
      <h2 className="text-2xl font-bold tracking-tight">Solo Practice Command Center</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Active Cases</h3>
            <p className="text-sm text-muted-foreground">Cases currently in progress</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">12</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Pending Invoices</h3>
            <p className="text-sm text-muted-foreground">Awaiting payment from clients</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">₹ 45,000</p>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow">
          <div className="p-6 flex flex-col space-y-1.5">
            <h3 className="font-semibold leading-none tracking-tight">Upcoming Hearings</h3>
            <p className="text-sm text-muted-foreground">Next 7 days</p>
          </div>
          <div className="p-6 pt-0">
            <p className="text-2xl font-bold">3</p>
          </div>
        </div>
      </div>
    </div>
  );
}
