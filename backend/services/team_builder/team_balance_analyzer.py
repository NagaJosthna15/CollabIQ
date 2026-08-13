class TeamBalanceAnalyzer:

    """
    Analyzes team size and responsibility distribution.

    Considers:
    - Estimated team size
    - Current selected team
    - Available candidate pool
    - Maximum feasible team size
    - Responsibilities per member
    - Workload balance
    """

    def analyze(
        self,
        project_requirements,
        selected_team,
        all_students
    ):


        estimated_team_size = (
            project_requirements.get(
                "estimated_team_size",
                0
            )
        )


        actual_team_size = len(
            selected_team
        )

        selected_students = set()

        for member in selected_team:

            student_name = (
                member[
                    "candidate"
                ][
                    "profile"
                ][
                    "student"
                ]
            )

            selected_students.add(
                student_name
            )

        available_candidates = []

        for student in all_students:

            student_name = student.get(
                "student"
            )

            if (
                student_name
                not in selected_students
            ):

                available_candidates.append(
                    student
                )

        available_candidate_count = len(
            available_candidates
        )

        maximum_feasible_team_size = (
            actual_team_size
            + available_candidate_count
        )

        if (
            estimated_team_size > 0
            and actual_team_size
            < estimated_team_size
        ):

            size_status = "understaffed"

        elif (
            estimated_team_size > 0
            and actual_team_size
            > estimated_team_size
        ):

            size_status = "overstaffed"

        else:

            size_status = "balanced"

        member_workload = []

        total_responsibilities = 0

        for member in selected_team:

            profile = member[
                "candidate"
            ][
                "profile"
            ]

            student_name = profile[
                "student"
            ]

            primary_role = member.get(
                "role"
            )

            secondary_roles = member.get(
                "secondary_roles",
                []
            )

            secondary_role_names = []

            for secondary in secondary_roles:

                role = secondary.get(
                    "role"
                )

                if role:

                    secondary_role_names.append(
                        role
                    )

            primary_count = (
                1
                if primary_role
                else 0
            )

            secondary_count = len(
                secondary_role_names
            )

            total_member_responsibilities = (
                primary_count
                + secondary_count
            )

            total_responsibilities += (
                total_member_responsibilities
            )

            member_workload.append({

                "student":
                    student_name,

                "primary_role":
                    primary_role,

                "secondary_roles":
                    secondary_role_names,

                "primary_count":
                    primary_count,

                "secondary_count":
                    secondary_count,

                "total_responsibilities":
                    total_member_responsibilities
            })

        overloaded_members = []

        for member in member_workload:

            if (
                member[
                    "total_responsibilities"
                ] > 3
            ):

                overloaded_members.append(
                    member["student"]
                )

     

        if overloaded_members:

            workload_status = "overloaded"

        else:

            workload_status = "manageable"


        if (
            estimated_team_size
            > actual_team_size
        ):

            members_needed = (
                estimated_team_size
                - actual_team_size
            )

        else:

            members_needed = 0

        additional_members_available = min(
            members_needed,
            available_candidate_count
        )

        recommendations = []

        if (
            size_status == "understaffed"
        ):

            if (
                available_candidate_count
                == 0
            ):

                recommendations.append(
                    "The team is understaffed, "
                    "but no additional candidates "
                    "are currently available."
                )

                recommendations.append(
                    "Consider recruiting new "
                    "candidates or expanding the "
                    "candidate pool."
                )

            elif (
                available_candidate_count
                < members_needed
            ):

                recommendations.append(
                    "The team is understaffed."
                )

                recommendations.append(
                    "Add "
                    + str(
                        additional_members_available
                    )
                    + " suitable candidate(s) "
                    "from the current candidate pool."
                )

                recommendations.append(
                    "The estimated team size "
                    "cannot be fully reached "
                    "with the current candidate pool."
                )

            else:

                recommendations.append(
                    "Consider adding "
                    + str(
                        members_needed
                    )
                    + " suitable candidate(s) "
                    "to match the estimated "
                    "team size."
                )

        if overloaded_members:

            recommendations.append(
                "Redistribute responsibilities "
                "because some team members have "
                "more than 3 responsibilities."
            )

        if not recommendations:

            recommendations.append(
                "Team size and responsibility "
                "distribution are currently "
                "manageable."
            )

        return {

            "estimated_team_size":
                estimated_team_size,

            "actual_team_size":
                actual_team_size,

            "available_candidate_count":
                available_candidate_count,

            "maximum_feasible_team_size":
                maximum_feasible_team_size,

            "members_needed":
                members_needed,

            "additional_members_available":
                additional_members_available,

            "size_status":
                size_status,

            "total_responsibilities":
                total_responsibilities,

            "member_workload":
                member_workload,

            "overloaded_members":
                overloaded_members,

            "workload_status":
                workload_status,

            "recommendations":
                recommendations
        }