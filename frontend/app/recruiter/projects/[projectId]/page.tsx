"use client";

import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowLeft,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  CircleAlert,
  FolderKanban,
  Loader2,
  Mail,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Users,
  X,
  Zap,
} from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Project = {
  _id?: string;
  id?: string;
  title: string;
  description?: string;
  required_skills?: string[];
  team_size?: number;
};

type Candidate = {
  name?: string;
  email?: string;
  role?: string;
  skills?: string[];
  scores?: {
    skill?: number;
    domain?: number;
  };
  profile?: {
    name?: string;
    email?: string;
    skills?: string[];
    recommended_role?: string;
  };
};

type Invitation = {
  candidate_name?: string;
  project_title?: string;
  role?: string;
  status?: string;
};

export default function ProjectDetailsPage() {
  const router = useRouter();
  const params = useParams();

  const projectId = String(params.projectId);

  const [project, setProject] = useState<Project | null>(null);
  const [matches, setMatches] = useState<Candidate[]>([]);
  const [invitations, setInvitations] = useState<Invitation[]>([]);
  const [smartTeam, setSmartTeam] = useState<any>(null);

  const [loading, setLoading] = useState(true);
  const [loadingMatches, setLoadingMatches] = useState(false);
  const [loadingInvitations, setLoadingInvitations] = useState(false);
  const [loadingTeam, setLoadingTeam] = useState(false);

  const [error, setError] = useState("");

  function getToken() {
    return (
      localStorage.getItem("collabiq_access_token") ||
      sessionStorage.getItem("collabiq_access_token")
    );
  }

  function handleAuthError(status: number) {
  if (status === 401) {
    localStorage.clear();
    sessionStorage.clear();
    router.push("/login");
    return true;
  }

  return false;
}

   async function loadProject() {
  const token = getToken();

  if (!token) {
    router.push("/login");
    return;
  }

  setLoading(true);
  setError("");

  try {
    const response = await fetch(`${API_URL}/projects`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (handleAuthError(response.status)) {
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

    const selectedProject = projectList.find(
      (item: Project) =>
        String(item._id || item.id) === projectId
    );

    if (!selectedProject) {
      throw new Error("Project not found");
    }

    setProject(selectedProject);
  } catch (err) {
    setError(
      err instanceof Error
        ? err.message
        : "Unable to load project"
    );
  } finally {
    setLoading(false);
  }
}

  async function loadMatches() {
  const token = getToken();

  if (!token) {
    router.push("/login");
    return;
  }

  setLoadingMatches(true);

  try {
    const response = await fetch(
      `${API_URL}/projects/${projectId}/matches`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (handleAuthError(response.status)) {
      return;
    }

    if (!response.ok) {
      throw new Error("Unable to load candidate matches");
    }

    const data = await response.json();

    const rawMatches = Array.isArray(data)
      ? data
      : Array.isArray(data.matches)
        ? data.matches
        : Array.isArray(data.candidates)
          ? data.candidates
          : [];

    setMatches(
      rawMatches.map((match: any) => ({
        name: match.student_name,
        scores: {
          skill: Number(match.match_score || 0) / 100,
          domain: Number(match.talent_score || 0) / 100,
        },
      }))
    );
  } catch {
    setMatches([]);
  } finally {
    setLoadingMatches(false);
  }
}     
  async function loadInvitations() {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    setLoadingInvitations(true);

    try {
      const response = await fetch(
        `${API_URL}/projects/${projectId}/invitations`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (handleAuthError(response.status)) {
        return;
      }

      if (!response.ok) {
        throw new Error("Unable to load invitations");
      }

      const data = await response.json();

      setInvitations(
        Array.isArray(data.invitations) ? data.invitations : []
      );
    } catch {
      setInvitations([]);
    } finally {
      setLoadingInvitations(false);
    }
  }

  async function buildSmartTeam() {
    const token = getToken();

    if (!token) {
      router.push("/login");
      return;
    }

    setLoadingTeam(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/projects/${projectId}/smart-team`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (handleAuthError(response.status)) {
        return;
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to build smart team"
        );
      }

      setSmartTeam(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to build smart team"
      );
    } finally {
      setLoadingTeam(false);
    }
  }

  useEffect(() => {
    loadProject();
    loadMatches();
    loadInvitations();
  }, [projectId]);

  const getCandidateName = (candidate: Candidate) =>
    candidate.name ||
    candidate.profile?.name ||
    "Candidate";

  const getCandidateSkills = (candidate: Candidate) =>
    candidate.skills ||
    candidate.profile?.skills ||
    [];

  const getCandidateRole = (candidate: Candidate) =>
    candidate.role ||
    candidate.profile?.recommended_role ||
    "Candidate";

  const getSkillScore = (candidate: Candidate) =>
    candidate.scores?.skill !== undefined
      ? Math.round(candidate.scores.skill * 100)
      : null;

  const getDomainScore = (candidate: Candidate) =>
    candidate.scores?.domain !== undefined
      ? Math.round(candidate.scores.domain * 100)
      : null;

  const getTeamMemberName = (member: any) => {
  return (
    member?.name ||
    member?.student_name ||
    member?.selected_student ||
    member?.selectedStudent ||
    (typeof member?.student === "string"
      ? member.student
      : "") ||
    member?.candidate_name ||
    member?.profile?.name ||
    member?.profile?.student ||
    member?.student_profile?.name ||
    member?.candidate?.name ||
    member?.candidate?.student ||
    member?.candidate?.profile?.name ||
    member?.candidate?.profile?.student ||
    "Team Member"
  );
};

  const getTeamMemberRole = (member: any) => {
    if (typeof member === "string") {
      return "Assigned member";
    }

    return (
      member?.role ||
      member?.assigned_role ||
      member?.responsibility ||
      member?.profile?.recommended_role ||
      "Assigned member"
    );
  };

  const getArrayLength = (value: any) =>
    Array.isArray(value) ? value.length : 0;

  const getTeamAnalysis = () => {
    if (!smartTeam) {
      return [];
    }

    const coverage = smartTeam.coverage || {};
    const skillGaps = Array.isArray(smartTeam.skill_gaps)
      ? smartTeam.skill_gaps
      : [];
    const additionalCandidates = Array.isArray(
      smartTeam.additional_candidates
    )
      ? smartTeam.additional_candidates
      : [];
    const team = Array.isArray(smartTeam.team)
      ? smartTeam.team
      : [];

    const missingRoles =
      coverage.missing_roles ||
      coverage.missingRoles ||
      coverage.uncovered_roles ||
      coverage.uncoveredRoles ||
      [];

    const coveragePercentage =
      coverage.coverage_percentage ??
      coverage.coveragePercentage ??
      coverage.role_coverage ??
      coverage.roleCoverage;

    const cards = [
      {
        key: "selected_team_members",
        label: "Selected Team Members",
        value: team.length || smartTeam.team_size || 0,
      },
      {
        key: "missing_roles",
        label: "Missing Roles",
        value: getArrayLength(missingRoles),
      },
      {
        key: "skill_gaps",
        label: "Skill Gaps",
        value: skillGaps.length,
      },
      {
        key: "additional_candidates",
        label: "Additional Candidates",
        value: additionalCandidates.length,
      },
    ];

    if (typeof coveragePercentage === "number") {
      cards.push({
        key: "coverage_percentage",
        label: "Role Coverage",
        value: coveragePercentage,
      });
    }

    return cards;
  };

  return (
    <main className="min-h-screen bg-[#05030d] text-white">
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute left-[8%] top-[8%] h-80 w-80 rounded-full bg-violet-600/10 blur-[140px]" />
        <div className="absolute right-[8%] top-[20%] h-96 w-96 rounded-full bg-fuchsia-600/10 blur-[150px]" />
        <div className="absolute bottom-0 left-[40%] h-80 w-80 rounded-full bg-cyan-500/10 blur-[140px]" />
      </div>

      <div className="pointer-events-none fixed inset-0 opacity-[0.06] [background-image:linear-gradient(rgba(255,255,255,0.2)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.2)_1px,transparent_1px)] [background-size:60px_60px]" />

      <header className="sticky top-0 z-30 border-b border-white/[0.07] bg-[#05030d]/80 backdrop-blur-2xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
          <button
            onClick={() => router.push("/recruiter/dashboard")}
            className="flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
          >
            <ArrowLeft size={16} />
            Dashboard
          </button>

          <div className="flex items-center gap-2">
            <span className="text-xl font-black">Collab</span>
            <span className="bg-gradient-to-r from-violet-400 via-fuchsia-400 to-cyan-300 bg-clip-text text-xl font-black text-transparent">
              IQ
            </span>
          </div>

          <button
            onClick={() => {
              loadProject();
              loadMatches();
              loadInvitations();
            }}
            className="rounded-xl border border-white/10 p-2.5 text-slate-400 transition hover:bg-white/[0.04] hover:text-white"
          >
            <RefreshCw
              size={17}
              className={loading ? "animate-spin" : ""}
            />
          </button>
        </div>
      </header>

      <div className="relative z-10 mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-10">
        {error && (
          <div className="mb-6 flex items-center gap-3 rounded-2xl border border-red-400/20 bg-red-500/[0.06] px-5 py-4 text-sm text-red-300">
            <CircleAlert size={18} />
            {error}
            <button
              onClick={() => setError("")}
              className="ml-auto"
            >
              <X size={16} />
            </button>
          </div>
        )}

        {loading ? (
          <div className="space-y-6">
            <div className="h-48 animate-pulse rounded-3xl border border-white/[0.07] bg-white/[0.025]" />
            <div className="grid gap-5 md:grid-cols-3">
              {[1, 2, 3].map((item) => (
                <div
                  key={item}
                  className="h-32 animate-pulse rounded-2xl border border-white/[0.07] bg-white/[0.025]"
                />
              ))}
            </div>
          </div>
        ) : !project ? (
          <div className="rounded-3xl border border-red-400/20 bg-red-500/[0.04] px-6 py-16 text-center">
            <CircleAlert className="mx-auto text-red-300" size={32} />
            <h2 className="mt-4 text-xl font-bold">
              Project not found
            </h2>
            <button
              onClick={() => router.push("/recruiter/dashboard")}
              className="mt-5 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold"
            >
              Back to Dashboard
            </button>
          </div>
        ) : (
          <>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-7 backdrop-blur-xl sm:p-9"
            >
              <div className="flex flex-col justify-between gap-7 lg:flex-row">
                <div className="max-w-3xl">
                  <div className="flex items-center gap-2 text-sm text-violet-400">
                    <Sparkles size={15} />
                    AI Recruitment Workspace
                  </div>

                  <h1 className="mt-3 text-3xl font-black tracking-tight sm:text-4xl">
                    {project.title}
                  </h1>

                  <p className="mt-4 text-sm leading-7 text-slate-400">
                    {project.description ||
                      "Project requirements and intelligent team optimization workspace."}
                  </p>
                </div>

                <div className="flex shrink-0 items-start">
                  <div className="rounded-2xl border border-emerald-400/10 bg-emerald-400/[0.05] px-4 py-3 text-sm text-emerald-400">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 size={16} />
                      Active Project
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-8 flex flex-wrap gap-2">
                {(project.required_skills || []).map((skill) => (
                  <span
                    key={skill}
                    className="rounded-full border border-violet-400/10 bg-violet-500/[0.08] px-3 py-1.5 text-xs text-violet-300"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </motion.div>

            <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {[
                {
                  icon: Users,
                  label: "Team Size",
                  value: project.team_size || "—",
                },
                {
                  icon: Users,
                  label: "Matched Candidates",
                  value: matches.length,
                },
                {
                  icon: Mail,
                  label: "Invitations",
                  value: invitations.length,
                },
                {
                  icon: Zap,
                  label: "AI Workspace",
                  value: "Ready",
                },
              ].map((stat, index) => {
                const Icon = stat.icon;

                return (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.06 }}
                    className="rounded-2xl border border-white/[0.08] bg-white/[0.025] p-5"
                  >
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-500/10 text-violet-300">
                      <Icon size={19} />
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

            <div className="mt-10 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
              <section className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-violet-400">
                      AI Matching
                    </div>

                    <h2 className="mt-2 text-xl font-bold">
                      Top Candidates
                    </h2>
                  </div>

                  <BrainCircuit
                    size={22}
                    className="text-violet-400"
                  />
                </div>

                {loadingMatches ? (
                  <div className="flex items-center justify-center py-14 text-sm text-slate-500">
                    <Loader2
                      size={18}
                      className="mr-2 animate-spin"
                    />
                    Loading matches...
                  </div>
                ) : matches.length === 0 ? (
                  <div className="py-14 text-center text-sm text-slate-500">
                    No candidate matches available.
                  </div>
                ) : (
                  <div className="mt-6 space-y-3">
                    {matches.slice(0, 8).map((candidate, index) => (
                      <div
                        key={`${candidate.profile?.name || candidate.name || "candidate"}-${index}`}
                        className="rounded-2xl border border-white/[0.07] bg-white/[0.02] p-4 transition hover:border-violet-400/20"
                      >
                        <div className="flex items-center gap-4">
                          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500/20 to-fuchsia-500/10 font-bold text-violet-300">
                            {getCandidateName(candidate)
                              .charAt(0)
                              .toUpperCase()}
                          </div>

                          <div className="min-w-0 flex-1">
                            <div className="font-semibold">
                              {getCandidateName(candidate)}
                            </div>

                            <div className="mt-1 text-xs text-slate-600">
                              {getCandidateRole(candidate)}
                            </div>
                          </div>

                          <ChevronRight
                            size={17}
                            className="text-slate-700"
                          />
                        </div>

                        <div className="mt-3 flex flex-wrap gap-1.5">
                          {getCandidateSkills(candidate)
                            .slice(0, 5)
                            .map((skill) => (
                              <span
                                key={skill}
                                className="rounded-full bg-violet-500/[0.08] px-2.5 py-1 text-[10px] text-violet-300"
                              >
                                {skill}
                              </span>
                            ))}
                        </div>

                        {(getSkillScore(candidate) !== null ||
                          getDomainScore(candidate) !== null) && (
                          <div className="mt-4 grid grid-cols-2 gap-3">
                            {getSkillScore(candidate) !== null && (
                              <div>
                                <div className="flex justify-between text-[10px] text-slate-600">
                                  <span>Skill Match</span>
                                  <span>
                                    {getSkillScore(candidate)}%
                                  </span>
                                </div>

                                <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-white/5">
                                  <div
                                    className="h-full rounded-full bg-violet-500"
                                    style={{
                                      width: `${getSkillScore(candidate)}%`,
                                    }}
                                  />
                                </div>
                              </div>
                            )}

                            {getDomainScore(candidate) !== null && (
                              <div>
                                <div className="flex justify-between text-[10px] text-slate-600">
                                  <span>Domain Match</span>
                                  <span>
                                    {getDomainScore(candidate)}%
                                  </span>
                                </div>

                                <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-white/5">
                                  <div
                                    className="h-full rounded-full bg-fuchsia-500"
                                    style={{
                                      width: `${getDomainScore(candidate)}%`,
                                    }}
                                  />
                                </div>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </section>

              <section className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-cyan-400">
                      AI Team Builder
                    </div>

                    <h2 className="mt-2 text-xl font-bold">
                      Smart Team
                    </h2>



                  </div>

                  <BrainCircuit
                    size={22}
                    className="text-cyan-300"
                  />
                </div>

                <p className="mt-4 text-sm leading-6 text-slate-500">
                  Let CollabIQ analyze the project requirements and
                  build a balanced team using the available candidates.
                </p>

                <button
                  onClick={buildSmartTeam}
                  disabled={loadingTeam}
                  className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 via-fuchsia-500 to-indigo-500 px-5 py-3 text-sm font-semibold transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loadingTeam ? (
                    <>
                      <Loader2
                        size={17}
                        className="animate-spin"
                      />
                      Building Smart Team...
                    </>
                  ) : (
                    <>
                      <Sparkles size={17} />
                      Build Smart Team
                    </>
                  )}
                </button>

                {smartTeam && (
                  <div className="mt-6 space-y-3">
                    <div className="rounded-2xl border border-emerald-400/10 bg-emerald-400/[0.04] p-4">
                      <div className="flex items-center gap-2 text-sm font-semibold text-emerald-300">
                        <CheckCircle2 size={16} />
                        Team Generated
                      </div>

                      <div className="mt-3 text-2xl font-black">
                        {Array.isArray(smartTeam.team)
                          ? smartTeam.team.length
                          : smartTeam.team_size || 0}
                      </div>

                      <div className="mt-1 text-xs text-slate-500">
                        Selected team members
                      </div>
                    </div>

                    {Array.isArray(smartTeam.team) &&
                      smartTeam.team.map(
                        (member: any, index: number) => (
                          <div
                            key={`${getTeamMemberName(member)}-${index}`}
                            className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-3"
                          >
                            <div className="text-sm font-semibold">
                              {getTeamMemberName(member)}
                            </div>

                        <div className="mt-1 text-xs text-slate-500">
                          {member?.role ||
                             member?.assigned_role ||
                            member?.candidate?.profile?.recommended_role ||
                            member?.candidate?.recommended_role ||
                           "Assigned member"}
                        </div>
                          </div>
                        )
                      )}
                  </div>
                )}
              </section>
            </div>

            <div className="mt-6 grid gap-6 lg:grid-cols-2">
              <section className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-emerald-400">
                      Team Analysis
                    </div>

                    <h2 className="mt-2 text-xl font-bold">
                      Success Analysis
                    </h2>
                  </div>

                  <ShieldCheck
                    size={22}
                    className="text-emerald-400"
                  />
                </div>

                {smartTeam ? (
                  <div className="mt-6 grid grid-cols-2 gap-3">
                    {getTeamAnalysis().map((item) => (
                      <div
                        key={item.key}
                        className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4"
                      >
                        <div className="text-[10px] uppercase tracking-wider text-slate-600">
                          {item.label}
                        </div>

                        <div className="mt-2 text-lg font-bold">
                          {typeof item.value === "number"
                            ? Number.isInteger(item.value)
                              ? item.value
                              : item.value.toFixed(2)
                            : String(item.value)}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-12 text-center text-sm text-slate-500">
                    Build a smart team to generate team analysis.
                  </div>
                )}
              </section>

              <section className="rounded-3xl border border-white/[0.08] bg-white/[0.025] p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-[0.25em] text-fuchsia-400">
                      Recruitment
                    </div>

                    <h2 className="mt-2 text-xl font-bold">
                      Invitation Status
                    </h2>
                  </div>

                  <Mail
                    size={22}
                    className="text-fuchsia-400"
                  />
                </div>

                {loadingInvitations ? (
                  <div className="flex items-center justify-center py-12 text-sm text-slate-500">
                    <Loader2
                      size={18}
                      className="mr-2 animate-spin"
                    />
                    Loading invitations...
                  </div>
                ) : invitations.length === 0 ? (
                  <div className="py-12 text-center text-sm text-slate-500">
                    No invitations sent yet.
                  </div>
                ) : (
                  <div className="mt-6 max-h-80 space-y-3 overflow-y-auto">
                    {invitations.map((invitation, index) => (
                      <div
                        key={`${invitation.candidate_name || "candidate"}-${index}`}
                        className="flex items-center justify-between rounded-xl border border-white/[0.07] bg-white/[0.02] p-4"
                      >
                        <div>
                          <div className="text-sm font-semibold">
                            {invitation.candidate_name ||
                              "Candidate"}
                          </div>

                          <div className="mt-1 text-xs text-slate-600">
                            {invitation.role ||
                              "Candidate invitation"}
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
                          {invitation.status || "invited"}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
    


