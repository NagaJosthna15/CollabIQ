
from urllib import response

from services.ai.gemini_service import (
    GeminiService
)

import json
import re
class ResponsibilityAgent:

    """
    AI agent responsible for assigning
    additional responsibilities to
    already selected team members
    using Gemini reasoning.
    """

    def __init__(self):
        self.gemini = GeminiService()


    def assign_secondary_role(
        self,
        role,
        selected_team
    ):

        
        prompt = self.build_prompt(
            role,
            selected_team
        )

        
        response = self.ask_gemini(
            prompt
        )
        print("\n========== GEMINI RESPONSE ==========")
        print(response)
        print("=====================================\n")


        result = self.parse_response(
            response
        )

        return result


    def build_prompt(
        self,
        role,
        selected_team
    ):
        team_details = ""

        for member in selected_team:
            team_details += self.format_student_profile(
                member
            )
            prompt = f"""
You are an AI Team Formation Expert.

A software project has one unassigned role.

Your responsibility is to analyze the already selected team
and decide who can best handle this additional responsibility.

Do not randomly choose.

Think carefully before making the decision.

While making the decision consider:

- Technical Skills
- Resume Skills
- Strong Domains
- Recommended Role
- Previous Experience
- Overall suitability

Missing Role:

{role}

Already Selected Team:

{team_details}

Return ONLY valid JSON.

Expected JSON format:

{{
    "selected_student": "",
    "confidence": 0,
    "reason": ""
}}

"""
        return prompt
    def format_student_profile(
    self,
    member
):
        candidate = member["candidate"]

        profile = candidate["profile"]
        return f"""
Student:
{profile["student"]}

Recommended Role:
{profile["recommended_role"]}

Skills:
{", ".join(profile["skills"])}

Resume Skills:
{", ".join(profile["resume_skills"])}

Strong Domains:
{", ".join(profile["strong_domains"])}

------------------------------------

"""    


    def ask_gemini(
    self,
    prompt
):
        return self.gemini.generate(
            prompt
    )
    def parse_response(
    self,
    response
):
        response = response.strip()

        response = response.replace(
            "```json",
            ""
        )
        response = response.replace(
           "```",
           ""
       )
        response = response.strip()
        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
       )
        if not re.match:
            raise ValueError(
                 "Gemini did not return valid JSON."
            )
        return json.loads(
             match.group()
       ) 
        

    