from services.recruiter_agent import RecruiterAgent

agent = RecruiterAgent()

profiles = agent.build_student_profiles()

for profile in profiles:
    print(profile)