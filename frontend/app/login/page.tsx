"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowLeft,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
  UserRound,
  Wifi,
} from "lucide-react";
import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(
          data.message || "Invalid email or password"
        );
      }

      const storage = remember
        ? localStorage
        : sessionStorage;

      storage.setItem(
        "collabiq_access_token",
        data.access_token
      );

      storage.setItem(
        "collabiq_role",
        data.role
      );

      storage.setItem(
        "collabiq_user_id",
        data.student_id
      );

      storage.setItem(
        "collabiq_user_name",
        data.student_name || ""
      );

      if (data.role === "recruiter") {
        router.push("/recruiter/dashboard");
      } else {
        router.push("/student/dashboard");
      }
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to connect to the server"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#05030d] text-white">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[8%] top-[12%] h-72 w-72 rounded-full bg-violet-600/20 blur-[130px]" />
        <div className="absolute right-[8%] top-[25%] h-80 w-80 rounded-full bg-cyan-500/10 blur-[140px]" />
        <div className="absolute bottom-[5%] left-[40%] h-72 w-72 rounded-full bg-fuchsia-600/15 blur-[130px]" />
      </div>

      <div className="pointer-events-none absolute inset-0 opacity-20 [background-image:linear-gradient(rgba(139,92,246,0.15)_1px,transparent_1px),linear-gradient(90deg,rgba(139,92,246,0.15)_1px,transparent_1px)] [background-size:48px_48px]" />

      <div className="pointer-events-none absolute inset-0 opacity-20">
        <motion.div
          animate={{
            x: [0, 30, -20, 0],
            y: [0, -20, 25, 0],
          }}
          transition={{
            duration: 18,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute left-[15%] top-[20%] h-28 w-28 rounded-full border border-cyan-400/30"
        />

        <motion.div
          animate={{
            x: [0, -35, 20, 0],
            y: [0, 25, -20, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute right-[14%] top-[35%] h-40 w-40 rounded-full border border-violet-400/25"
        />

        <motion.div
          animate={{
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 30,
            repeat: Infinity,
            ease: "linear",
          }}
          className="absolute bottom-[18%] left-[18%] h-16 w-16 rounded-full border border-fuchsia-400/30"
        />
      </div>

      <header className="absolute left-0 right-0 top-0 z-20">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6">
          <Link href="/" className="group flex items-center">
            <span className="text-2xl font-black tracking-tight">
              Collab
            </span>
            <span className="bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300 bg-clip-text text-2xl font-black text-transparent">
              IQ
            </span>
          </Link>

          <Link
            href="/"
            className="group flex items-center gap-2 text-sm text-slate-400 transition hover:text-white"
          >
            <ArrowLeft
              size={16}
              className="transition group-hover:-translate-x-1"
            />
            Back to home
          </Link>
        </div>
      </header>

      <section className="relative z-10 flex min-h-screen items-center justify-center px-5 py-28">
        <motion.div
          initial={{
            opacity: 0,
            y: 35,
            scale: 0.97,
          }}
          animate={{
            opacity: 1,
            y: 0,
            scale: 1,
          }}
          transition={{
            duration: 0.7,
            ease: "easeOut",
          }}
          className="w-full max-w-md"
        >
          <div className="relative">
            <div className="absolute -inset-[1px] rounded-[28px] bg-gradient-to-b from-violet-400/60 via-fuchsia-500/20 to-cyan-400/40 opacity-70 blur-[1px]" />

            <div className="relative overflow-hidden rounded-[28px] border border-white/10 bg-[#090713]/90 p-7 shadow-2xl shadow-violet-950/40 backdrop-blur-2xl sm:p-9">
              <div className="absolute left-0 right-0 top-0 h-px bg-gradient-to-r from-transparent via-violet-400 to-transparent" />

              <div className="absolute left-4 top-4 h-5 w-5 border-l border-t border-cyan-400/60" />
              <div className="absolute right-4 top-4 h-5 w-5 border-r border-t border-cyan-400/60" />
              <div className="absolute bottom-4 left-4 h-5 w-5 border-b border-l border-cyan-400/60" />
              <div className="absolute bottom-4 right-4 h-5 w-5 border-b border-r border-cyan-400/60" />

              <div className="mb-8 text-center">
                <motion.div
                  animate={{
                    boxShadow: [
                      "0 0 0 rgba(139,92,246,0)",
                      "0 0 35px rgba(139,92,246,0.22)",
                      "0 0 0 rgba(139,92,246,0)",
                    ],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                  }}
                  className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border border-violet-400/20 bg-violet-500/10"
                >
                  <Sparkles className="text-violet-300" size={25} />
                </motion.div>

                <div className="mt-6 text-[10px] font-bold uppercase tracking-[0.4em] text-cyan-400">
                  Access
                </div>

                <h1 className="mt-2 text-3xl font-black tracking-tight">
                  Welcome Back
                </h1>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  Sign in to continue to your CollabIQ workspace.
                </p>

                <div className="mt-4 flex items-center justify-center gap-2 text-[10px] uppercase tracking-[0.2em] text-slate-600">
                  <Wifi size={11} className="text-emerald-400" />
                  System Ready
                </div>
              </div>

              <form onSubmit={handleLogin} className="space-y-5">
                <div>
                  <label className="mb-2 flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">
                    <UserRound size={12} />
                    User Identification
                  </label>

                  <div className="group relative">
                    <Mail
                      size={17}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 transition group-focus-within:text-violet-400"
                    />

                    <input
                      type="email"
                      value={email}
                      onChange={(event) =>
                        setEmail(event.target.value)
                      }
                      placeholder="Enter email address"
                      required
                      autoComplete="email"
                      className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-violet-400/60 focus:bg-violet-500/[0.04] focus:ring-4 focus:ring-violet-500/10"
                    />
                  </div>
                </div>

                <div>
                  <label className="mb-2 flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">
                    <LockKeyhole size={12} />
                    Secret Code
                  </label>

                  <div className="group relative">
                    <LockKeyhole
                      size={17}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 transition group-focus-within:text-cyan-400"
                    />

                    <input
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(event) =>
                        setPassword(event.target.value)
                      }
                      placeholder="Enter password"
                      required
                      autoComplete="current-password"
                      className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] pl-11 pr-12 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-cyan-400/60 focus:bg-cyan-500/[0.03] focus:ring-4 focus:ring-cyan-500/10"
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(!showPassword)
                      }
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-600 transition hover:text-white"
                    >
                      {showPassword ? (
                        <EyeOff size={17} />
                      ) : (
                        <Eye size={17} />
                      )}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs">
                  <label className="flex cursor-pointer items-center gap-2 text-slate-500">
                    <input
                      type="checkbox"
                      checked={remember}
                      onChange={(event) =>
                        setRemember(event.target.checked)
                      }
                      className="h-3.5 w-3.5 accent-violet-500"
                    />
                    Remember session
                  </label>

                  <button
                    type="button"
                    className="text-violet-400 transition hover:text-violet-300"
                  >
                    Forgot password?
                  </button>
                </div>

                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{
                        opacity: 0,
                        y: -8,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      exit={{
                        opacity: 0,
                        y: -8,
                      }}
                      className="rounded-xl border border-red-400/20 bg-red-500/[0.07] px-4 py-3 text-sm text-red-300"
                    >
                      {error}
                    </motion.div>
                  )}
                </AnimatePresence>

                <motion.button
                  whileHover={{
                    scale: 1.01,
                  }}
                  whileTap={{
                    scale: 0.98,
                  }}
                  disabled={loading}
                  type="submit"
                  className="relative flex h-12 w-full items-center justify-center overflow-hidden rounded-xl bg-gradient-to-r from-violet-500 via-fuchsia-500 to-indigo-500 font-bold shadow-lg shadow-violet-500/20 transition disabled:cursor-not-allowed disabled:opacity-60"
                >
                  <span className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 transition duration-500 hover:translate-x-full hover:opacity-100" />

                  {loading ? (
                    <span className="flex items-center gap-3">
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                      Authenticating...
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      Initialize Login
                      <ArrowLeft
                        size={16}
                        className="rotate-180"
                      />
                    </span>
                  )}
                </motion.button>
              </form>

              <div className="my-7 flex items-center gap-3">
                <div className="h-px flex-1 bg-white/[0.08]" />
                <span className="text-[9px] uppercase tracking-[0.25em] text-slate-700">
                  Secure Access
                </span>
                <div className="h-px flex-1 bg-white/[0.08]" />
              </div>

              <div className="flex items-center justify-center gap-2 text-xs text-slate-600">
                <ShieldCheck
                  size={14}
                  className="text-emerald-400"
                />
                Protected authentication
              </div>

              <div className="mt-6 text-center text-sm text-slate-500">
                New to CollabIQ?{" "}
                <Link
                  href="/register"
                  className="font-semibold text-violet-400 transition hover:text-fuchsia-400"
                >
                  Create account
                </Link>
              </div>

              <div className="mt-6 text-center text-[9px] uppercase tracking-[0.25em] text-slate-700">
                Intelligent Collaboration System
              </div>
            </div>
          </div>
        </motion.div>
      </section>
    </main>
  );
}