from services.student_intelligence import build_student_profile


class StudentProfileBuilder:

    def build_profile(self, student):
        return build_student_profile(student)

    def build_profiles(self, students):

        profiles = []

        for student in students:
            try:
                profile = self.build_profile(student)
                profiles.append(profile)

            except Exception as e:
                print(f"Error building profile for {student.get('name')}: {e}")

        return profiles