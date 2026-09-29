"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000";

export default function RegisterPage() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [cgpa, setCgpa] = useState("");
  const [skills, setSkills] = useState("");
  const [interests, setInterests] = useState("");
  const [projectsCompleted, setProjectsCompleted] =
    useState("");
  const [githubUsername, setGithubUsername] =
    useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleRegister(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setError("");

    if (
      !name ||
      !email ||
      !password ||
      !cgpa ||
      !skills ||
      !interests ||
      !projectsCompleted ||
      !githubUsername
    ) {
      setError("Please fill all fields");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/auth/register`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            email,
            password,
            cgpa: Number(cgpa),
            skills: skills
              .split(",")
              .map((skill) => skill.trim())
              .filter(Boolean),
            interests: interests
              .split(",")
              .map((interest) => interest.trim())
              .filter(Boolean),
            projects_completed: Number(
              projectsCompleted
            ),
            github_username: githubUsername.trim(),
          }),
        }
      );

      const data = await response.json();

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
            : "Registration failed";

        throw new Error(detail);
      }

      router.push("/login");
    } catch (err: any) {
      setError(
        err.message || "Unable to create account"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#07050f] px-6 py-12 text-white">
      <div className="mx-auto flex min-h-[85vh] max-w-md items-center justify-center">
        <div className="w-full rounded-3xl border border-white/10 bg-white/[0.03] p-8 shadow-2xl backdrop-blur-xl">
          <div className="mb-8 text-center">
            <Link
              href="/"
              className="text-3xl font-black tracking-tight"
            >
              Collab <span className="text-fuchsia-400">IQ</span>
            </Link>

            <h1 className="mt-8 text-3xl font-bold">
              Create Student Account
            </h1>

            <p className="mt-2 text-sm text-slate-400">
              Join CollabIQ and build smarter teams.
            </p>
          </div>

          <form
            onSubmit={handleRegister}
            className="space-y-5"
          >
            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Full Name
              </label>

              <input
                value={name}
                onChange={(event) =>
                  setName(event.target.value)
                }
                placeholder="Enter your name"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Email
              </label>

              <input
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                placeholder="Enter your email"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Password
              </label>

              <input
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="Minimum 8 characters"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
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
                value={cgpa}
                onChange={(event) =>
                  setCgpa(event.target.value)
                }
                placeholder="Enter your CGPA"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Skills
              </label>

              <input
                value={skills}
                onChange={(event) =>
                  setSkills(event.target.value)
                }
                placeholder="Python, Machine Learning, SQL"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
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
                value={interests}
                onChange={(event) =>
                  setInterests(event.target.value)
                }
                placeholder="AI, Web Development, Data Science"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
              />

              <p className="mt-1 text-xs text-slate-500">
                Separate interests with commas
              </p>
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Projects Completed
              </label>

              <input
                type="number"
                min="0"
                value={projectsCompleted}
                onChange={(event) =>
                  setProjectsCompleted(
                    event.target.value
                  )
                }
                placeholder="0"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                GitHub Username
              </label>

              <input
                value={githubUsername}
                onChange={(event) =>
                  setGithubUsername(event.target.value)
                }
                placeholder="Your GitHub username"
                className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-white outline-none transition focus:border-violet-500"
              />
            </div>

            {error && (
              <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-4 py-3 font-semibold transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Creating Account..."
                : "Create Account"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-500">
            Already have an account?{" "}
            <Link
              href="/login"
              className="font-semibold text-violet-400 transition hover:text-fuchsia-400"
            >
              Login
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}