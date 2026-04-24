"use client";

import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";
import { Building2, Users, FileCheck, IndianRupee, LayoutDashboard } from "lucide-react";
import { usePathname } from "next/navigation";

const firmLinks = [
  { title: "Firm Dashboard", href: "/firm", icon: LayoutDashboard },
  { title: "Team Workspace", href: "/firm/team", icon: Users },
  { title: "Conflict Check", href: "/firm/conflict", icon: FileCheck },
  { title: "Firm Billing", href: "/firm/billing", icon: IndianRupee },
  { title: "Settings", href: "/firm/settings", icon: Building2 },
];

export default function FirmLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar links={firmLinks} currentPath={pathname} />
      <div className="flex flex-1 flex-col">
        <Header title="Law Firm Enterprise Workspace" />
        <main className="flex-1 overflow-auto bg-muted/20 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
