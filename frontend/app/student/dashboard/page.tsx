"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  Bell,
  BriefcaseBusiness,
  CheckCircle2,
  Code2,
  Edit3,
  LogOut,
  Save,
  UserRound,
  X,
  XCircle,
} from "lucide-react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export default function StudentDashboard() {
  const router = useRouter();

  const [student, setStudent] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [githubData, setGithubData] = useState<any>(null);
  const [githubLoading, setGithubLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editOpen, setEditOpen] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    cgpa: "",
    skills: "",
    interests: "",
    projects_completed: "",
    github_username: "",
  });

  useEffect(() => {
    const token = localStorage.getItem(
      "collabiq_access_token"
    );

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
        setGithubLoading(true);

try {
  const githubResponse = await fetch(
    `${API_URL}/students/me/github-projects`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  if (githubResponse.ok) {
    const githubResult = await githubResponse.json();
    setGithubData(githubResult);
  }
} catch {
  setGithubData(null);
} finally {
  setGithubLoading(false);
}

        setForm({
          name: data.name || "",
          email: data.email || "",
          cgpa:
            data.cgpa !== undefined
              ? String(data.cgpa)
              : "",
          skills: Array.isArray(data.skills)
            ? data.skills.join(", ")
            : "",
          interests: Array.isArray(data.interests)
            ? data.interests.join(", ")
            : "",
          projects_completed:
            data.projects_completed !== undefined
              ? String(data.projects_completed)
              : "",
          github_username:
            data.github_username || "",
        });
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

  function openEditProfile() {
    setSuccess("");
    setError("");

    setForm({
      name: student?.name || "",
      email: student?.email || "",
      cgpa:
        student?.cgpa !== undefined
          ? String(student.cgpa)
          : "",
      skills: Array.isArray(student?.skills)
        ? student.skills.join(", ")
        : "",
      interests: Array.isArray(student?.interests)
        ? student.interests.join(", ")
        : "",
      projects_completed:
        student?.projects_completed !== undefined
          ? String(student.projects_completed)
          : "",
      github_username:
        student?.github_username || "",
    });

    setEditOpen(true);
  }

  function closeEditProfile() {
    if (!saving) {
      setEditOpen(false);
    }
  }

  async function handleSaveProfile(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const token = localStorage.getItem(
      "collabiq_access_token"
    );

    if (!token) {
      router.push("/login");
      return;
    }

    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const response = await fetch(
        `${API_URL}/students/me`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            name: form.name.trim(),
            email: form.email.trim(),
            cgpa: Number(form.cgpa),
            skills: form.skills
              .split(",")
              .map((skill) => skill.trim())
              .filter(Boolean),
            interests: form.interests
              .split(",")
              .map((interest) => interest.trim())
              .filter(Boolean),
            projects_completed: Number(
              form.projects_completed
            ),
            github_username:
              form.github_username.trim(),
          }),
        }
      );

      const data = await response.json();

      if (response.status === 401) {
        localStorage.clear();
        sessionStorage.clear();
        router.push("/login");
        return;
      }

      if (!response.ok) {
        const detail = Array.isArray(data.detail)
          ? data.detail
              .map((item: any) =>
                typeof item === "string"
                  ? item
                  : item?.msg || "Invalid input"
              )
              .join(", ")
          : typeof data.detail === "string"
            ? data.detail
            : "Unable to update profile";

        throw new Error(detail);
      }

      const updatedStudent =
        data.student || data;

      setStudent(updatedStudent);

      setForm({
        name: updatedStudent.name || "",
        email: updatedStudent.email || "",
        cgpa:
          updatedStudent.cgpa !== undefined
            ? String(updatedStudent.cgpa)
            : "",
        skills: Array.isArray(
          updatedStudent.skills
        )
          ? updatedStudent.skills.join(", ")
          : "",
        interests: Array.isArray(
          updatedStudent.interests
        )
          ? updatedStudent.interests.join(", ")
          : "",
        projects_completed:
          updatedStudent.projects_completed !==
          undefined
            ? String(
                updatedStudent.projects_completed
              )
            : "",
        github_username:
          updatedStudent.github_username || "",
      });

      setEditOpen(false);
      setSuccess("Profile updated successfully");
    } catch (err: any) {
      setError(
        err.message || "Unable to update profile"
      );
    } finally {
      setSaving(false);
    }
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

          <div className="flex items-center gap-3">
            <button
              onClick={openEditProfile}
              className="flex items-center gap-2 rounded-xl border border-violet-400/30 bg-violet-500/10 px-4 py-2 text-sm font-medium text-violet-300 transition hover:border-violet-400/60 hover:bg-violet-500/20"
            >
              <Edit3 size={16} />
              Edit Profile
            </button>

            <button
              onClick={handleLogout}
              className="flex items-center gap-2 rounded-xl border border-white/10 px-4 py-2 text-sm text-slate-300 transition hover:border-red-400/40 hover:text-red-400"
            >
              <LogOut size={16} />
              Logout
            </button>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-6 py-10">
        {error && !editOpen && (
          <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/10 px-5 py-4 text-red-400">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-6 rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-5 py-4 text-emerald-400">
            {success}
          </div>
        )}

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
         <div className="mt-8 rounded-3xl border border-white/10 bg-white/[0.03] p-7">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Code2 className="text-cyan-400" />
              <div>
                <h2 className="text-xl font-bold">
                  GitHub Projects
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  {githubData?.username
                    ? `@${githubData.username}`
                    : "Connect your GitHub profile"}
                </p>
              </div>
            </div>

            {githubData?.repositories?.length > 0 && (
              <span className="rounded-full border border-cyan-400/20 bg-cyan-400/10 px-3 py-1 text-xs text-cyan-300">
                {githubData.repositories.length} Repositories
              </span>
            )}
          </div>

          {githubLoading ? (
            <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-6 text-center text-sm text-slate-400">
              Loading GitHub projects...
            </div>
          ) : githubData?.repositories?.length > 0 ? (
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {githubData.repositories.map(
                (repo: any, index: number) => (
                  <div
                    key={`${repo.name}-${index}`}
                    className="rounded-2xl border border-white/10 bg-black/20 p-5 transition hover:border-cyan-400/30"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <h3 className="font-semibold text-white">
                        {repo.name || "Untitled Repository"}
                      </h3>

                      {repo.language && (
                        <span className="shrink-0 rounded-full bg-violet-400/10 px-3 py-1 text-xs text-violet-300">
                          {repo.language}
                        </span>
                      )}
                    </div>

                    <p className="mt-3 text-sm leading-6 text-slate-400">
                      {repo.description ||
                        "No description available"}
                    </p>
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-6 text-center">
              <Code2 className="mx-auto text-slate-500" size={28} />
              <p className="mt-3 text-sm text-slate-400">
                No GitHub projects found.
              </p>
              <p className="mt-1 text-xs text-slate-600">
                Add your GitHub username in Edit Profile.
              </p>
            </div>
          )}
        </div>
      </section>

      {editOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 py-6 backdrop-blur-sm">
          <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-3xl border border-violet-500/20 bg-[#0d0918] p-7 shadow-2xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-cyan-400">
                  Profile Settings
                </p>

                <h2 className="mt-2 text-2xl font-bold">
                  Edit Profile
                </h2>
              </div>

              <button
                onClick={closeEditProfile}
                className="rounded-xl border border-white/10 p-2 text-slate-400 transition hover:text-white"
              >
                <X size={20} />
              </button>
            </div>

            <form
              onSubmit={handleSaveProfile}
              className="mt-7 space-y-5"
            >
              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm text-slate-300">
                    Full Name
                  </label>

                  <input
                    value={form.name}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        name: event.target.value,
                      })
                    }
                    className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm text-slate-300">
                    Email
                  </label>

                  <input
                    type="email"
                    value={form.email}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        email: event.target.value,
                      })
                    }
                    className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm text-slate-300">
                    CGPA
                  </label>

                  <input
                    type="number"
                    min="0"
                    max="10"
                    step="0.01"
                    value={form.cgpa}
                    onChange={(event) =>
                      setForm({
                        ...form,
                        cgpa: event.target.value,
                      })
                    }
                    className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                  />
                </div>

                <div>
                  <label className="mb-2 block text-sm text-slate-300">
                    Projects Completed
                  </label>

                  <input
                    type="number"
                    min="0"
                    value={
                      form.projects_completed
                    }
                    onChange={(event) =>
                      setForm({
                        ...form,
                        projects_completed:
                          event.target.value,
                      })
                    }
                    className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                  />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-300">
                  Skills
                </label>

                <input
                  value={form.skills}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      skills: event.target.value,
                    })
                  }
                  placeholder="Python, Machine Learning, SQL"
                  className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                />

                <p className="mt-1 text-xs text-slate-500">
                  Separate skills with commas
                </p>
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-300">
                  Interests
                </label>

                <input
                  value={form.interests}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      interests: event.target.value,
                    })
                  }
                  placeholder="AI, Data Science"
                  className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                />

                <p className="mt-1 text-xs text-slate-500">
                  Separate interests with commas
                </p>
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-300">
                  GitHub Username
                </label>

                <input
                  value={form.github_username}
                  onChange={(event) =>
                    setForm({
                      ...form,
                      github_username:
                        event.target.value,
                    })
                  }
                  placeholder="Your GitHub username"
                  className="w-full rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-white outline-none focus:border-violet-500"
                />
              </div>

              {error && (
                <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                  {error}
                </div>
              )}

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={closeEditProfile}
                  disabled={saving}
                  className="rounded-xl border border-white/10 px-5 py-3 text-sm text-slate-300 transition hover:bg-white/5 disabled:opacity-50"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  disabled={saving}
                  className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-3 text-sm font-semibold transition hover:opacity-90 disabled:opacity-50"
                >
                  <Save size={16} />
                  {saving
                    ? "Saving..."
                    : "Save Changes"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}