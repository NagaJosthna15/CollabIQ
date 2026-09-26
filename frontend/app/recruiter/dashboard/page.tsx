"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowRight,
  Bell,
  BriefcaseBusiness,
  CheckCircle2,
  ChevronDown,
  FolderKanban,
  LogOut,
  Menu,
  Plus,
  RefreshCw,
  Sparkles,
  Users,
  X,
  Zap,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Project = {
  _id?: string;
  id?: string;
  title: string;
  description?: string;
  required_skills?: string[];
  team_size?: number;
  created_by?: string;
};

export default function RecruiterDashboard() {
  const router = useRouter();

  const [projects, setProjects] = useState<Project[]>([]);
  const [userName, setUserName] = useState("Recruiter");
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showCreate, setShowCreate] = useState(false);
  const [error, setError] = useState("");
  const [activePanel, setActivePanel] = useState<
  "candidates" | "invitations" | "notifications" | "profile" | null
>(null);

const [candidates, setCandidates] = useState<any[]>([]);
const [invitations, setInvitations] = useState<any[]>([]);
const [panelLoading, setPanelLoading] = useState(false);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [skills, setSkills] = useState("");
  const [teamSize, setTeamSize] = useState("4");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState("");
  const [createSuccess, setCreateSuccess] = useState("");

  function getToken() {
    return (
      localStorage.getItem("collabiq_access_token") ||
      sessionStorage.getItem("collabiq_access_token")
    );
  }

  async function loadProjects(showRefresh = false) {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    if (showRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    setError("");

    try {
      const response = await fetch(`${API_URL}/projects`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 401 || response.status === 403) {
        localStorage.clear();
        sessionStorage.clear();
        router.push("/login");
        return;
      }

      if (!response.ok) {
        throw new Error("Unable to load projects");
      }

      const data = await response.json();

      const projectList = Array.isArray(data)
        ? data
        : Array.isArray(data.projects)
          ? data.projects
          : [];

      setProjects(projectList);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load projects"
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }
  async function loadCandidates() {
  const token = getToken();

  if (!token) {
    router.push("/login");
    return;
  }

  setPanelLoading(true);

  try {
    const response = await fetch(`${API_URL}/students`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Unable to load candidates");
    }

    const data = await response.json();

    setCandidates(
      Array.isArray(data)
        ? data
        : Array.isArray(data.students)
          ? data.students
          : []
    );
  } catch {
    setCandidates([]);
  } finally {
    setPanelLoading(false);
  }
}
async function loadInvitations() {
  const token = getToken();

  if (!token) {
    router.push("/login");
    return;
  }

  setPanelLoading(true);

  try {
    const results = [];

    for (const project of projects) {
      const projectId = project._id || project.id;

      if (!projectId) {
        continue;
      }

      const response = await fetch(
        `${API_URL}/projects/${projectId}/invitations`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        continue;
      }

      const data = await response.json();

      const projectInvitations = Array.isArray(data.invitations)
        ? data.invitations
        : [];

      results.push(
        ...projectInvitations.map((invitation: any) => ({
          ...invitation,
          project_title:
            invitation.project_title || project.title,
        }))
      );
    }

    setInvitations(results);
  } catch {
    setInvitations([]);
  } finally {
    setPanelLoading(false);
  }
}

  useEffect(() => {
    const storedName =
      localStorage.getItem("collabiq_user_name") ||
      sessionStorage.getItem("collabiq_user_name");

    const storedRole =
      localStorage.getItem("collabiq_role") ||
      sessionStorage.getItem("collabiq_role");

    if (!storedName || storedRole !== "recruiter") {
      router.push("/login");
      return;
    }

    setUserName(storedName);
    loadProjects();
  }, [router]);

  async function createProject() {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    setCreateError("");
    setCreateSuccess("");

    if (title.trim().length < 2) {
      setCreateError("Project title must contain at least 2 characters.");
      return;
    }

    if (description.trim().length < 10) {
      setCreateError(
        "Project description must contain at least 10 characters."
      );
      return;
    }

    const requiredSkills = skills
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean);

    if (requiredSkills.length === 0) {
      setCreateError("Add at least one required skill.");
      return;
    }

    setCreating(true);

    try {
      const response = await fetch(`${API_URL}/projects`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          required_skills: requiredSkills,
          team_size: Number(teamSize),
        }),
      });

      const data = await response.json();

      if (response.status === 401 || response.status === 403) {
        localStorage.clear();
        sessionStorage.clear();
        router.push("/login");
        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail || data.message || "Unable to create project"
        );
      }

      setCreateSuccess("Project created successfully.");

      setTitle("");
      setDescription("");
      setSkills("");
      setTeamSize("4");

      await loadProjects(true);

      setTimeout(() => {
        setShowCreate(false);
        setCreateSuccess("");
      }, 900);
    } catch (err) {
      setCreateError(
        err instanceof Error
          ? err.message
          : "Unable to create project"
      );
    } finally {
      setCreating(false);
    }
  }

  function logout() {
    localStorage.removeItem("collabiq_access_token");
    localStorage.removeItem("collabiq_role");
    localStorage.removeItem("collabiq_user_id");
    localStorage.removeItem("collabiq_user_name");

    sessionStorage.removeItem("collabiq_access_token");
    sessionStorage.removeItem("collabiq_role");
    sessionStorage.removeItem("collabiq_user_id");
    sessionStorage.removeItem("collabiq_user_name");

    router.push("/login");
  }

  return (
    <main className="min-h-screen overflow-hidden bg-[#05030d] text-white">
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute left-[10%] top-[10%] h-80 w-80 rounded-full bg-violet-600/10 blur-[140px]" />
        <div className="absolute right-[5%] top-[25%] h-96 w-96 rounded-full bg-fuchsia-600/10 blur-[150px]" />
        <div className="absolute bottom-0 left-[40%] h-80 w-80 rounded-full bg-cyan-500/10 blur-[140px]" />
      </div>

      <div className="pointer-events-none fixed inset-0 opacity-[0.07] [background-image:linear-gradient(rgba(255,255,255,0.2)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.2)_1px,transparent_1px)] [background-size:60px_60px]" />

      <aside className="fixed bottom-0 left-0 top-0 z-40 hidden w-64 border-r border-white/[0.07] bg-[#080610]/80 backdrop-blur-2xl lg:block">
        <div className="flex h-full flex-col p-6">
          <div className="flex items-center px-3 py-2">
            <span className="text-2xl font-black">Collab</span>
            <span className="bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300 bg-clip-text text-2xl font-black text-transparent">
              IQ
            </span>
          </div>

          <div className="mt-12">
            <div className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.25em] text-slate-600">
              Workspace
            </div>

            <div className="rounded-xl border border-violet-400/10 bg-violet-500/[0.08] px-4 py-3 text-sm font-medium text-violet-300">
              <div className="flex items-center gap-3">
                <FolderKanban size={17} />
                Dashboard
              </div>
            </div>

            <button
              onClick={() => setShowCreate(true)}
              className="mt-2 w-full rounded-xl px-4 py-3 text-left text-sm text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
            >
              <div className="flex items-center gap-3">
                <Plus size={17} />
                Create Project
              </div>
            </button>

            <button
  onClick={() => {
    setActivePanel("candidates");
    loadCandidates();
  }}
  className={`mt-2 w-full rounded-xl px-4 py-3 text-left text-sm transition ${
    activePanel === "candidates"
      ? "bg-violet-500/[0.08] text-violet-300"
      : "text-slate-400 hover:bg-white/[0.04] hover:text-white"
  }`}
>
  <div className="flex items-center gap-3">
    <Users size={17} />
    Candidates
  </div>
</button>

            <button
  onClick={() => {
    setActivePanel("invitations");
    loadInvitations();
  }}
  className={`mt-2 w-full rounded-xl px-4 py-3 text-left text-sm transition ${
    activePanel === "invitations"
      ? "bg-violet-500/[0.08] text-violet-300"
      : "text-slate-400 hover:bg-white/[0.04] hover:text-white"
  }`}
>
  <div className="flex items-center gap-3">
    <Bell size={17} />
    Invitations
  </div>
</button>
          </div>

          <div className="mt-auto">
            <button
              onClick={logout}
              className="w-full rounded-xl px-4 py-3 text-left text-sm text-slate-500 transition hover:bg-red-500/[0.06] hover:text-red-300"
            >
              <div className="flex items-center gap-3">
                <LogOut size={17} />
                Logout
              </div>
            </button>
          </div>
        </div>
      </aside>

      <section className="relative z-10 min-h-screen lg:pl-64">
        <header className="sticky top-0 z-30 border-b border-white/[0.07] bg-[#05030d]/75 backdrop-blur-2xl">
          <div className="flex items-center justify-between px-5 py-4 sm:px-8">
            <div className="flex items-center gap-3 lg:hidden">
              <span className="text-xl font-black">Collab</span>
              <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text font-black text-transparent">
                IQ
              </span>
            </div>

            <div className="hidden lg:block">
              <div className="text-sm text-slate-500">
                Recruiter Workspace
              </div>
              <div className="text-xs text-slate-700">
                Intelligent Team Optimization
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button
  onClick={() => {
  const opening =
    activePanel !== "notifications";

  setActivePanel(
    opening ? "notifications" : null
  );

  if (opening) {
    loadCandidates();
  }
}}
  className="relative rounded-xl border border-white/10 bg-white/[0.02] p-2.5 text-slate-400 transition hover:text-white"
>
  <Bell size={18} />

  <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-fuchsia-400" />
</button>

              <div className="hidden h-8 w-px bg-white/10 sm:block" />

              <button
  onClick={() =>
    setActivePanel(
      activePanel === "profile"
        ? null
        : "profile"
    )
  }
  className="flex items-center gap-3 rounded-xl p-1.5 transition hover:bg-white/[0.04]"
>
  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-fuchsia-500 text-sm font-bold">
    {userName.charAt(0).toUpperCase()}
  </div>

  <div className="hidden text-left sm:block">
    <div className="text-sm font-semibold">
      {userName}
    </div>

    <div className="text-[10px] uppercase tracking-wider text-slate-600">
      Recruiter
    </div>
  </div>

  <ChevronDown
    size={15}
    className="hidden text-slate-600 sm:block"
  />
</button>
            </div>
          </div>
        </header>

        <div className="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">
              <div>
                <div className="flex items-center gap-2 text-sm text-violet-400">
                  <Sparkles size={15} />
                  AI Recruitment Workspace
                </div>

                <h1 className="mt-3 text-3xl font-black tracking-tight sm:text-4xl">
                  Good to see you,{" "}
                  <span className="bg-gradient-to-r from-violet-400 to-fuchsia-400 bg-clip-text text-transparent">
                    {userName}
                  </span>
                  .
                </h1>

                <p className="mt-3 max-w-xl text-sm leading-7 text-slate-500">
                  Manage your projects, discover suitable candidates and build
                  intelligent teams from one workspace.
                </p>
              </div>

              <button
                onClick={() => setShowCreate(true)}
                className="group flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold shadow-lg shadow-violet-500/15 transition hover:-translate-y-0.5"
              >
                <Plus size={17} />
                Create Project
                <ArrowRight
                  size={15}
                  className="transition group-hover:translate-x-1"
                />
              </button>
            </div>
          </motion.div>

          <div className="mt-10 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {[
              {
                icon: BriefcaseBusiness,
                label: "Total Projects",
                value: projects.length,
              },
              {
                icon: Users,
                label: "Team Capacity",
                value: projects.reduce(
                  (total, project) =>
                    total + (project.team_size || 0),
                  0
                ),
              },
              {
                icon: Zap,
                label: "AI Workspace",
                value: "Active",
              },
              {
                icon: CheckCircle2,
                label: "System",
                value: "Ready",
              },
            ].map((stat, index) => {
              const Icon = stat.icon;

              return (
                <motion.div
                  key={stat.label}
                  initial={{
                    opacity: 0,
                    y: 20,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                  }}
                  transition={{
                    delay: index * 0.08,
                  }}
                  className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-5 backdrop-blur-xl"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-300">
                      <Icon size={19} />
                    </div>

                    <div className="text-[10px] uppercase tracking-[0.2em] text-slate-700">
                      Live
                    </div>
                  </div>

                  <div className="mt-5 text-2xl font-black">
                    {stat.value}
                  </div>

                  <div className="mt-1 text-xs text-slate-500">
                    {stat.label}
                  </div>
                </motion.div>
              );
            })}
          </div>

          <div className="mt-12">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-violet-400">
                  Project Workspace
                </div>

                <h2 className="mt-2 text-2xl font-bold">
                  Your Projects
                </h2>
              </div>

              <button
                onClick={() => loadProjects(true)}
                className="flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2 text-xs text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
              >
                <RefreshCw
                  size={14}
                  className={refreshing ? "animate-spin" : ""}
                />
                Refresh
              </button>
            </div>

            {error && (
              <div className="mt-6 rounded-2xl border border-red-400/20 bg-red-500/[0.06] px-5 py-4 text-sm text-red-300">
                {error}
              </div>
            )}

            {loading ? (
              <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                {[1, 2, 3].map((item) => (
                  <div
                    key={item}
                    className="h-64 animate-pulse rounded-2xl border border-white/[0.06] bg-white/[0.02]"
                  />
                ))}
              </div>
            ) : projects.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-8 rounded-3xl border border-dashed border-white/10 bg-white/[0.02] px-6 py-16 text-center"
              >
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-violet-500/10 text-violet-300">
                  <FolderKanban size={25} />
                </div>

                <h3 className="mt-5 text-xl font-bold">
                  No projects yet
                </h3>

                <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
                  Create your first project and let CollabIQ analyze the
                  available candidates.
                </p>

                <button
                  onClick={() => setShowCreate(true)}
                  className="mt-6 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold"
                >
                  Create Your First Project
                </button>
              </motion.div>
            ) : (
              <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                {projects.map((project, index) => {
                  const projectId =
                    project._id || project.id || "";

                  return (
                    <motion.div
                      key={projectId || index}
                      initial={{
                        opacity: 0,
                        y: 20,
                      }}
                      animate={{
                        opacity: 1,
                        y: 0,
                      }}
                      transition={{
                        delay: index * 0.08,
                      }}
                      whileHover={{
                        y: -5,
                      }}
                      className="group rounded-2xl border border-white/[0.08] bg-white/[0.025] p-6 backdrop-blur-xl transition hover:border-violet-400/20"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500/15 to-fuchsia-500/10 text-violet-300">
                          <FolderKanban size={20} />
                        </div>

                        <div className="rounded-full border border-emerald-400/10 bg-emerald-400/[0.05] px-2.5 py-1 text-[10px] font-medium text-emerald-400">
                          Active
                        </div>
                      </div>

                      <h3 className="mt-6 line-clamp-2 text-xl font-bold">
                        {project.title}
                      </h3>

                      <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-500">
                        {project.description ||
                          "Project requirements and team optimization workspace."}
                      </p>

                      <div className="mt-5 flex items-center justify-between border-t border-white/[0.06] pt-5">
                        <div>
                          <div className="text-[10px] uppercase tracking-wider text-slate-700">
                            Team Size
                          </div>
                          <div className="mt-1 flex items-center gap-2 text-sm font-semibold">
                            <Users size={14} className="text-violet-400" />
                            {project.team_size || "—"}
                          </div>
                        </div>

                        <button
                          onClick={() =>
                            router.push(
                              `/recruiter/projects/${projectId}`
                            )
                          }
                          className="flex items-center gap-2 text-xs font-semibold text-violet-400 transition hover:text-fuchsia-400"
                        >
                          Open
                          <ArrowRight
                            size={14}
                            className="transition group-hover:translate-x-1"
                          />
                        </button>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
        <AnimatePresence>
  {activePanel && (
    <motion.div
      initial={{ opacity: 0, x: 30 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 30 }}
      className="fixed right-5 top-20 z-[90] w-[360px] max-w-[calc(100vw-40px)] rounded-2xl border border-white/10 bg-[#0b0815]/95 p-5 shadow-2xl shadow-black/50 backdrop-blur-2xl"
    >
      <div className="flex items-center justify-between">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-violet-400">
            CollabIQ
          </div>

          <h3 className="mt-1 text-lg font-bold">
            {activePanel === "candidates" && "Candidates"}
            {activePanel === "invitations" && "Invitations"}
            {activePanel === "notifications" && "Notifications"}
            {activePanel === "profile" && "Recruiter Profile"}
          </h3>
        </div>

        <button
          onClick={() => setActivePanel(null)}
          className="rounded-lg p-2 text-slate-500 transition hover:bg-white/5 hover:text-white"
        >
          <X size={17} />
        </button>
      </div>

      {activePanel === "candidates" && (
        <div className="mt-5 max-h-[60vh] space-y-3 overflow-y-auto">
          {panelLoading ? (
            <div className="py-8 text-center text-sm text-slate-500">
              Loading candidates...
            </div>
          ) : candidates.length === 0 ? (
            <div className="py-8 text-center text-sm text-slate-500">
              No candidates available.
            </div>
          ) : (
            candidates.map((candidate, index) => (
              <div
                key={candidate._id || candidate.id || index}
                className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-4"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-500/10 text-sm font-bold text-violet-300">
                    {(
                      candidate.name ||
                      candidate.student ||
                      "C"
                    )
                      .charAt(0)
                      .toUpperCase()}
                  </div>

                  <div className="min-w-0">
                    <div className="truncate text-sm font-semibold">
                      {candidate.name ||
                        candidate.student ||
                        "Candidate"}
                    </div>

                    <div className="truncate text-xs text-slate-600">
                      {candidate.email || "Registered candidate"}
                    </div>
                  </div>
                </div>

                <div className="mt-3 flex flex-wrap gap-1.5">
                  {(candidate.skills || [])
                    .slice(0, 4)
                    .map((skill: string) => (
                      <span
                        key={skill}
                        className="rounded-full bg-violet-500/[0.08] px-2 py-1 text-[10px] text-violet-300"
                      >
                        {skill}
                      </span>
                    ))}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activePanel === "invitations" && (
        <div className="mt-5 max-h-[60vh] space-y-3 overflow-y-auto">
          {panelLoading ? (
            <div className="py-8 text-center text-sm text-slate-500">
              Loading invitations...
            </div>
          ) : invitations.length === 0 ? (
            <div className="py-8 text-center text-sm text-slate-500">
              No invitations found.
            </div>
          ) : (
            invitations.map((invitation, index) => (
              <div
                key={
                  invitation.invitation_id || index
                }
                className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold">
                      {invitation.candidate_name}
                    </div>

                    <div className="mt-1 text-xs text-slate-600">
                      {invitation.project_title}
                    </div>

                    <div className="mt-2 text-xs text-slate-500">
                      {invitation.role}
                    </div>
                  </div>

                  <span
                    className={`rounded-full px-2.5 py-1 text-[10px] ${
                      invitation.status === "accepted"
                        ? "bg-emerald-500/10 text-emerald-400"
                        : invitation.status === "rejected"
                          ? "bg-red-500/10 text-red-400"
                          : "bg-violet-500/10 text-violet-300"
                    }`}
                  >
                    {invitation.status}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activePanel === "notifications" && (
        <div className="mt-5">
          <div className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-4">
            <div className="flex gap-3">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-violet-500/10 text-violet-300">
                <Sparkles size={17} />
              </div>

              <div>
                <div className="text-sm font-semibold">
                  Workspace Ready
                </div>

                <p className="mt-1 text-xs leading-5 text-slate-500">
                  Your CollabIQ recruitment workspace is active.
                </p>
              </div>
            </div>
          </div>

          <div className="mt-3 rounded-xl border border-white/[0.07] bg-white/[0.025] p-4">
            <div className="flex gap-3">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-fuchsia-500/10 text-fuchsia-300">
                <Users size={17} />
              </div>

              <div>
                <div className="text-sm font-semibold">
                  Candidate Pool
                </div>

                <p className="mt-1 text-xs leading-5 text-slate-500">
                  {candidates.length || "Registered"} candidates are available in the system.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {activePanel === "profile" && (
        <div className="mt-5">
          <div className="flex items-center gap-4 rounded-xl border border-white/[0.07] bg-white/[0.025] p-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-fuchsia-500 text-lg font-bold">
              {userName.charAt(0).toUpperCase()}
            </div>

            <div>
              <div className="font-semibold">
                {userName}
              </div>

              <div className="mt-1 text-xs uppercase tracking-wider text-slate-600">
                Recruiter
              </div>
            </div>
          </div>

          <button
            onClick={logout}
            className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-red-400/10 bg-red-500/[0.05] px-4 py-3 text-sm text-red-300 transition hover:bg-red-500/[0.1]"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      )}
    </motion.div>
  )}
</AnimatePresence>
      </section>

      <AnimatePresence>
        {showCreate && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] flex items-center justify-center bg-black/70 px-5 backdrop-blur-md"
            onMouseDown={(event) => {
              if (event.target === event.currentTarget) {
                setShowCreate(false);
              }
            }}
          >
            <motion.div
              initial={{
                opacity: 0,
                scale: 0.96,
                y: 20,
              }}
              animate={{
                opacity: 1,
                scale: 1,
                y: 0,
              }}
              exit={{
                opacity: 0,
                scale: 0.96,
                y: 20,
              }}
              className="relative max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-3xl border border-white/10 bg-[#0b0815] p-7 shadow-2xl shadow-violet-950/50 sm:p-8"
            >
              <button
                onClick={() => setShowCreate(false)}
                className="absolute right-5 top-5 rounded-xl p-2 text-slate-500 transition hover:bg-white/5 hover:text-white"
              >
                <X size={18} />
              </button>

              <div className="mb-7">
                <div className="flex items-center gap-2 text-sm text-violet-400">
                  <Sparkles size={15} />
                  AI Project Workspace
                </div>

                <h2 className="mt-2 text-2xl font-black">
                  Create Project
                </h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  Define your project requirements so CollabIQ can build the
                  right team.
                </p>
              </div>

              <div className="space-y-5">
                <div>
                  <label className="mb-2 block text-xs font-semibold text-slate-400">
                    Project Title
                  </label>

                  <input
                    value={title}
                    onChange={(event) =>
                      setTitle(event.target.value)
                    }
                    placeholder="e.g. AI Healthcare Assistant"
                    className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-violet-400/50 focus:ring-4 focus:ring-violet-500/10"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-xs font-semibold text-slate-400">
                    Project Description
                  </label>

                  <textarea
                    value={description}
                    onChange={(event) =>
                      setDescription(event.target.value)
                    }
                    placeholder="Describe the project, goals and technical requirements..."
                    rows={4}
                    className="w-full resize-none rounded-xl border border-white/10 bg-white/[0.025] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-violet-400/50 focus:ring-4 focus:ring-violet-500/10"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-xs font-semibold text-slate-400">
                    Required Skills
                  </label>

                  <input
                    value={skills}
                    onChange={(event) =>
                      setSkills(event.target.value)
                    }
                    placeholder="Python, React, MongoDB, Machine Learning"
                    className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-violet-400/50 focus:ring-4 focus:ring-violet-500/10"
                  />

                  <p className="mt-2 text-[11px] text-slate-600">
                    Separate skills using commas.
                  </p>
                </div>

                <div>
                  <label className="mb-2 block text-xs font-semibold text-slate-400">
                    Team Size
                  </label>

                  <input
                    type="number"
                    min="1"
                    value={teamSize}
                    onChange={(event) =>
                      setTeamSize(event.target.value)
                    }
                    className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition focus:border-violet-400/50 focus:ring-4 focus:ring-violet-500/10"
                  />
                </div>

                {createError && (
                  <div className="rounded-xl border border-red-400/20 bg-red-500/[0.06] px-4 py-3 text-sm text-red-300">
                    {createError}
                  </div>
                )}

                {createSuccess && (
                  <div className="flex items-center gap-2 rounded-xl border border-emerald-400/20 bg-emerald-500/[0.06] px-4 py-3 text-sm text-emerald-300">
                    <CheckCircle2 size={16} />
                    {createSuccess}
                  </div>
                )}

                <button
                  onClick={createProject}
                  disabled={creating}
                  className="flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 via-fuchsia-500 to-indigo-500 font-semibold shadow-lg shadow-violet-500/15 transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {creating ? (
                    <>
                      <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white" />
                      Creating Project...
                    </>
                  ) : (
                    <>
                      Create Project
                      <ArrowRight size={17} />
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}