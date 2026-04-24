"use client";

import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";
import { FileText, Search, Scale, FileSignature, HelpCircle } from "lucide-react";
import { usePathname } from "next/navigation";

const citizenLinks = [
  { title: "Dashboard", href: "/citizen", icon: Search },
  { title: "Translate Document", href: "/citizen/translate", icon: FileText },
  { title: "Find an Advocate", href: "/citizen/advocates", icon: Scale },
  { title: "Draft Letter", href: "/citizen/draft", icon: FileSignature },
  { title: "Consumer Help", href: "/citizen/consumer", icon: HelpCircle },
];

export default function CitizenLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar links={citizenLinks} currentPath={pathname} />
      <div className="flex flex-1 flex-col">
        <Header title="Citizen Portal" />
        <main className="flex-1 overflow-auto bg-muted/20 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
