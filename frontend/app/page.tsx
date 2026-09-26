"use client";

import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  CheckCircle2,
  ChevronDown,
  Code2,
  Layers3,
  Menu,
  Network,
  Sparkles,
  Target,
  Users,
  X,
  Zap,
} from "lucide-react";
import Link from "next/link";
import { useState } from "react";

const features = [
  {
    icon: Brain,
    title: "AI Candidate Matching",
    text: "Analyze skills, resumes and project requirements to identify candidates aligned with project needs.",
  },
  {
    icon: Network,
    title: "Smart Team Formation",
    text: "Build balanced teams by mapping candidates to required project roles and responsibilities.",
  },
  {
    icon: Target,
    title: "Skill Gap Detection",
    text: "Detect missing capabilities and identify genuine skill gaps before project execution begins.",
  },
  {
    icon: Sparkles,
    title: "AI Responsibility Assignment",
    text: "Use AI-assisted reasoning to assign additional responsibilities to suitable team members.",
  },
  {
    icon: Users,
    title: "Candidate Invitations",
    text: "Invite selected candidates and manage acceptance, rejection and replacement workflows.",
  },
  {
    icon: Layers3,
    title: "Team Success Analysis",
    text: "Analyze skill coverage, role balance, compatibility, risks and overall team capability.",
  },
];

const steps = [
  {
    number: "01",
    title: "Create Project",
    text: "Define the project, required skills, preferred roles and team size.",
  },
  {
    number: "02",
    title: "Analyze Candidates",
    text: "CollabIQ evaluates registered candidate profiles and their capabilities.",
  },
  {
    number: "03",
    title: "Build Smart Team",
    text: "AI maps candidates to roles and detects remaining skill gaps.",
  },
  {
    number: "04",
    title: "Invite & Collaborate",
    text: "Send invitations and track candidate responses from one platform.",
  },
];

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <main className="min-h-screen overflow-hidden bg-[#070511] text-white">
      <div className="pointer-events-none fixed inset-0 -z-0">
        <div className="absolute left-[10%] top-[10%] h-80 w-80 rounded-full bg-violet-600/20 blur-[140px] animate-pulse" />
        <div className="absolute right-[5%] top-[30%] h-96 w-96 rounded-full bg-fuchsia-600/15 blur-[150px] animate-pulse" />
        <div className="absolute bottom-[5%] left-[40%] h-72 w-72 rounded-full bg-indigo-600/15 blur-[130px] animate-pulse" />
      </div>

      <div className="pointer-events-none fixed inset-0 -z-0 opacity-[0.08] [background-image:linear-gradient(rgba(255,255,255,0.15)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.15)_1px,transparent_1px)] [background-size:70px_70px]" />

      <nav className="fixed left-0 right-0 top-0 z-50 border-b border-white/[0.08] bg-[#070511]/70 backdrop-blur-2xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <Link href="/" className="group flex items-center gap-1">
            <span className="text-2xl font-black tracking-tight">Collab</span>
            <span className="bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300 bg-clip-text text-2xl font-black text-transparent">
              IQ
            </span>
          </Link>

          <div className="hidden items-center gap-8 md:flex">
            <a href="#features" className="text-sm text-slate-400 transition hover:text-white">
              Features
            </a>
            <a href="#workflow" className="text-sm text-slate-400 transition hover:text-white">
              Workflow
            </a>
            <a href="#about" className="text-sm text-slate-400 transition hover:text-white">
              About
            </a>

            <Link
              href="/login"
              className="rounded-xl border border-white/10 px-5 py-2.5 text-sm font-medium text-slate-200 transition hover:border-violet-400/40 hover:bg-white/5"
            >
              Login
            </Link>

            <Link
              href="/register"
              className="group flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-semibold shadow-lg shadow-violet-500/20 transition hover:-translate-y-0.5"
            >
              Get Started
              <ArrowRight size={16} className="transition group-hover:translate-x-1" />
            </Link>
          </div>

          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="rounded-xl border border-white/10 p-2.5 md:hidden"
          >
            {menuOpen ? <X size={21} /> : <Menu size={21} />}
          </button>
        </div>

        {menuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            className="border-t border-white/10 bg-[#070511] px-6 py-6 md:hidden"
          >
            <div className="flex flex-col gap-5">
              <a href="#features" onClick={() => setMenuOpen(false)} className="text-slate-300">
                Features
              </a>
              <a href="#workflow" onClick={() => setMenuOpen(false)} className="text-slate-300">
                Workflow
              </a>
              <a href="#about" onClick={() => setMenuOpen(false)} className="text-slate-300">
                About
              </a>
              <Link href="/login" className="text-slate-300">
                Login
              </Link>
              <Link
                href="/register"
                className="rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-center font-semibold"
              >
                Get Started
              </Link>
            </div>
          </motion.div>
        )}
      </nav>

      <section className="relative z-10 px-6 pb-24 pt-40">
        <div className="mx-auto max-w-6xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="mx-auto inline-flex items-center gap-2 rounded-full border border-violet-400/20 bg-violet-500/[0.08] px-5 py-2 text-sm text-violet-300 backdrop-blur-xl"
          >
            <Sparkles size={15} />
            AI-Powered Team Intelligence
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.15 }}
            className="mx-auto mt-8 max-w-5xl text-5xl font-black leading-[1.05] tracking-tight sm:text-6xl lg:text-8xl"
          >
            Build the
            <span className="block bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300 bg-clip-text text-transparent">
              Right Team
            </span>
            <span className="block">for Every Project</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="mx-auto mt-8 max-w-2xl text-base leading-8 text-slate-400 sm:text-lg"
          >
            CollabIQ analyzes skills, resumes, experience and project
            requirements to intelligently connect the right people with the
            right roles.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 25 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.45 }}
            className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
          >
            <Link
              href="/register"
              className="group flex items-center gap-2 rounded-2xl bg-gradient-to-r from-violet-500 via-fuchsia-500 to-indigo-500 px-7 py-4 font-semibold shadow-2xl shadow-violet-500/25 transition duration-300 hover:-translate-y-1"
            >
              Start Building Teams
              <ArrowRight size={18} className="transition group-hover:translate-x-1" />
            </Link>

            <a
              href="#workflow"
              className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/[0.03] px-7 py-4 font-semibold text-slate-200 backdrop-blur-xl transition hover:border-violet-400/30 hover:bg-white/[0.06]"
            >
              Explore Workflow
              <ChevronDown size={18} />
            </a>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.6 }}
            className="relative mx-auto mt-20 max-w-5xl"
          >
            <div className="absolute -inset-10 rounded-[40px] bg-gradient-to-r from-violet-500/10 via-fuchsia-500/10 to-cyan-500/10 blur-3xl" />

            <div className="relative grid gap-4 sm:grid-cols-3">
              {[
                {
                  icon: Brain,
                  value: "AI",
                  label: "Candidate Intelligence",
                },
                {
                  icon: Users,
                  value: "Smart",
                  label: "Team Formation",
                },
                {
                  icon: Zap,
                  value: "Real-time",
                  label: "Project Decisions",
                },
              ].map((item, index) => {
                const Icon = item.icon;

                return (
                  <motion.div
                    key={item.label}
                    animate={{ y: [0, -7, 0] }}
                    transition={{
                      duration: 4,
                      delay: index * 0.5,
                      repeat: Infinity,
                    }}
                    className="rounded-3xl border border-white/10 bg-white/[0.035] p-7 text-left shadow-2xl backdrop-blur-2xl"
                  >
                    <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/10 text-violet-300">
                      <Icon size={23} />
                    </div>

                    <div className="text-2xl font-bold">{item.value}</div>
                    <div className="mt-1 text-sm text-slate-500">{item.label}</div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        </div>
      </section>

      <section id="features" className="relative z-10 border-t border-white/[0.07] px-6 py-28">
        <div className="mx-auto max-w-7xl">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-2xl"
          >
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-violet-400">
              Platform Intelligence
            </p>

            <h2 className="mt-4 text-4xl font-black tracking-tight sm:text-5xl">
              Everything you need to build smarter teams.
            </h2>

            <p className="mt-5 leading-8 text-slate-400">
              One intelligent platform for candidate analysis, team formation,
              skill-gap detection and project collaboration.
            </p>
          </motion.div>

          <div className="mt-16 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => {
              const Icon = feature.icon;

              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.08 }}
                  whileHover={{ y: -8 }}
                  className="group rounded-3xl border border-white/[0.08] bg-white/[0.025] p-7 backdrop-blur-xl transition hover:border-violet-400/25 hover:bg-white/[0.045]"
                >
                  <div className="mb-7 flex h-13 w-13 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/10 text-violet-300">
                    <Icon size={23} />
                  </div>

                  <h3 className="text-xl font-bold">{feature.title}</h3>

                  <p className="mt-3 leading-7 text-slate-400">
                    {feature.text}
                  </p>

                  <div className="mt-6 h-px w-0 bg-gradient-to-r from-violet-500 to-fuchsia-500 transition-all duration-500 group-hover:w-full" />
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      <section id="workflow" className="relative z-10 border-t border-white/[0.07] px-6 py-28">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-fuchsia-400">
              How It Works
            </p>

            <h2 className="mt-4 text-4xl font-black tracking-tight sm:text-5xl">
              From project idea to intelligent team.
            </h2>
          </div>

          <div className="mt-16 grid gap-5 md:grid-cols-4">
            {steps.map((step, index) => (
              <motion.div
                key={step.number}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="relative rounded-3xl border border-white/[0.08] bg-white/[0.025] p-7"
              >
                <div className="text-sm font-black text-violet-400">
                  {step.number}
                </div>

                <h3 className="mt-5 text-xl font-bold">{step.title}</h3>

                <p className="mt-3 leading-7 text-slate-400">
                  {step.text}
                </p>

                {index < steps.length - 1 && (
                  <div className="absolute -right-3 top-1/2 hidden h-6 w-6 -translate-y-1/2 items-center justify-center rounded-full border border-white/10 bg-[#070511] text-violet-400 md:flex">
                    <ArrowRight size={13} />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section id="about" className="relative z-10 border-t border-white/[0.07] px-6 py-28">
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="relative mx-auto max-w-5xl overflow-hidden rounded-[32px] border border-violet-400/15 bg-gradient-to-br from-violet-500/10 via-fuchsia-500/[0.04] to-cyan-500/[0.08] p-10 text-center sm:p-16"
        >
          <div className="absolute left-1/2 top-0 h-40 w-72 -translate-x-1/2 rounded-full bg-violet-500/20 blur-[100px]" />

          <div className="relative">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-500/15 text-violet-300">
              <Code2 size={25} />
            </div>

            <h2 className="mt-7 text-4xl font-black tracking-tight sm:text-5xl">
              Intelligent Collaboration.
              <br />
              <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">
                Better Teams.
              </span>
            </h2>

            <p className="mx-auto mt-6 max-w-2xl leading-8 text-slate-400">
              CollabIQ connects project requirements with candidate
              capabilities to help organizations create balanced,
              skill-aware teams.
            </p>

            <Link
              href="/register"
              className="mt-9 inline-flex items-center gap-2 rounded-2xl bg-white px-7 py-4 font-semibold text-slate-950 transition hover:-translate-y-1 hover:bg-slate-200"
            >
              Get Started
              <ArrowRight size={17} />
            </Link>
          </div>
        </motion.div>
      </section>

      <footer className="relative z-10 border-t border-white/[0.07] px-6 py-9">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 text-sm text-slate-500 sm:flex-row">
          <div>
            © 2026 CollabIQ
          </div>

          <div>
            Intelligent Collaboration & Team Optimization
          </div>
        </div>
      </footer>
    </main>
  );
}