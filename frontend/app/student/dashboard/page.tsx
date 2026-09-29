"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Bell,
  BriefcaseBusiness,
  CheckCircle2,
  Code2,
  LogOut,
  UserRound,
  XCircle,
} from "lucide-react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export default function StudentDashboard() {
  const router = useRouter();

  const [student, setStudent] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token =
      localStorage.getItem("collabiq_access_token");

    if (!token) {
      router.push("/login");
      return;
    }

    async function loadProfile() {
      try {
        const response = await fetch(
          `${API_URL}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.status === 401) {
          localStorage.clear();
          sessionStorage.clear();
          router.push("/login");
          return;
        }

        if (!response.ok) {
          throw new Error("Unable to load profile");
        }

        const data = await response.json();
        setStudent(data);
      } catch {
        setError("Unable to load your profile");
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, [router]);

  function handleLogout() {
    localStorage.clear();
    sessionStorage.clear();
    router.push("/login");
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#07050f] px-6 py-12 text-white">
        <div className="mx-auto max-w-6xl">
          <div className="h-10 w-48 animate-pulse rounded-xl bg-white/10" />
          <div className="mt-10 h-48 animate-pulse rounded-3xl bg-white/5" />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#07050f] text-white">
      <header className="border-b border-white/10 bg-black/20 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <div className="text-2xl font-black">
              Collab{" "}
              <span className="text-fuchsia-400">
                IQ
              </span>
            </div>

            <p className="mt-1 text-xs uppercase tracking-[0.3em] text-cyan-400">
              Student Workspace
            </p>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-300 transition hover:border-red-400/40 hover:text-red-400"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-6 py-10">
        <div className="rounded-3xl border border-violet-500/20 bg-white/[0.03] p-8 shadow-2xl">
          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">
                Welcome back
              </p>

              <h1 className="mt-3 text-4xl font-black">
                {student?.name || "Student"}
              </h1>

              <p className="mt-3 text-slate-400">
                Manage your profile and stay updated
                with your CollabIQ opportunities.
              </p>
            </div>

            <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-violet-500/30 bg-violet-500/10">
              <UserRound
                size={28}
                className="text-violet-400"
              />
            </div>
          </div>
        </div>

        {error && (
          <div className="mt-6 rounded-2xl border border-red-500/20 bg-red-500/10 px-5 py-4 text-red-400">
            {error}
          </div>
        )}

        <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <Code2 className="text-cyan-400" />
            <p className="mt-5 text-sm text-slate-500">
              Skills
            </p>
            <p className="mt-1 text-3xl font-bold">
              {student?.skills?.length || 0}
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <BriefcaseBusiness className="text-violet-400" />
            <p className="mt-5 text-sm text-slate-500">
              Projects
            </p>
            <p className="mt-1 text-3xl font-bold">
              {student?.projects_completed || 0}
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <UserRound className="text-fuchsia-400" />
            <p className="mt-5 text-sm text-slate-500">
              CGPA
            </p>
            <p className="mt-1 text-3xl font-bold">
              {student?.cgpa ?? "-"}
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
            <Bell className="text-emerald-400" />
            <p className="mt-5 text-sm text-slate-500">
              Role
            </p>
            <p className="mt-1 text-2xl font-bold capitalize">
              {student?.role || "Student"}
            </p>
          </div>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-7">
            <div className="flex items-center gap-3">
              <Code2 className="text-cyan-400" />
              <h2 className="text-xl font-bold">
                Your Skills
              </h2>
            </div>

            <div className="mt-6 flex flex-wrap gap-3">
              {(student?.skills || []).map(
                (skill: string, index: number) => (
                  <span
                    key={`${skill}-${index}`}
                    className="rounded-full border border-violet-400/20 bg-violet-400/10 px-4 py-2 text-sm text-violet-300"
                  >
                    {skill}
                  </span>
                )
              )}
            </div>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-7">
            <div className="flex items-center gap-3">
              <BriefcaseBusiness className="text-fuchsia-400" />
              <h2 className="text-xl font-bold">
                Your Interests
              </h2>
            </div>

            <div className="mt-6 flex flex-wrap gap-3">
              {(student?.interests || []).map(
                (
                  interest: string,
                  index: number
                ) => (
                  <span
                    key={`${interest}-${index}`}
                    className="rounded-full border border-fuchsia-400/20 bg-fuchsia-400/10 px-4 py-2 text-sm text-fuchsia-300"
                  >
                    {interest}
                  </span>
                )
              )}
            </div>
          </div>
        </div>

        <div className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-7">
          <div className="flex items-center gap-3">
            <Bell className="text-cyan-400" />
            <h2 className="text-xl font-bold">
              Recruitment Status
            </h2>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <CheckCircle2 className="text-emerald-400" />
              <p className="mt-4 text-sm text-slate-500">
                Profile Status
              </p>
              <p className="mt-1 font-semibold text-emerald-400">
                Active
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <Bell className="text-violet-400" />
              <p className="mt-4 text-sm text-slate-500">
                Invitations
              </p>
              <p className="mt-1 font-semibold">
                Check for updates
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-5">
              <XCircle className="text-slate-500" />
              <p className="mt-4 text-sm text-slate-500">
                Current Status
              </p>
              <p className="mt-1 font-semibold">
                Available
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}