"use client";

import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";
import { Briefcase, MessageSquare, Lock, FileSearch, IndianRupee } from "lucide-react";
import { usePathname } from "next/navigation";

const advocateLinks = [
  { title: "Dashboard", href: "/advocate", icon: Briefcase },
  { title: "AI Lawyer Chat", href: "/advocate/chat", icon: MessageSquare },
  { title: "Digital Vault", href: "/advocate/vault", icon: Lock },
  { title: "Law Search", href: "/advocate/search", icon: FileSearch },
  { title: "Invoicing", href: "/advocate/invoicing", icon: IndianRupee },
];

export default function AdvocateLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar links={advocateLinks} currentPath={pathname} />
      <div className="flex flex-1 flex-col">
        <Header title="Advocate Command Center" />
        <main className="flex-1 overflow-auto bg-muted/20 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
