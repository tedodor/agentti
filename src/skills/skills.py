from pathlib import Path
import subprocess

class Skill:
    def __init__(self, md_file: Path):
        with md_file.open() as f:
            name = None
            description = None
            scripts: dict[str, str] = {}
            for line in f:
                if line.startswith("#name:"):
                    name = line[len("#name:"):].strip()
                elif line.startswith("#description:"):
                    description = line[len("#description:"):].strip()
                elif line.startswith("#script:"):
                    script_name = line[len("#script:"):].strip()
                    script_content = []
                    for script_line in f:
                        if script_line.startswith("#end_script"):
                            break
                        script_content.append(script_line)
                    scripts[script_name] = "".join(script_content)

        # Add scripts from the scripts/ folder
        scripts_dir = md_file.parent / "scripts"
        if scripts_dir.exists():
            for script_file in scripts_dir.iterdir():
                if script_file.is_file():
                    scripts[script_file.stem] = str(script_file)

        self.name = name
        self.description = description
        self.scripts = scripts

    def run_script(self, script_name: str, *args, **kwargs):
        if script_name not in self.scripts:
            raise ValueError(f"Script '{script_name}' not found in skill '{self.name}'.")
        script_path = self.scripts[script_name]

        result = subprocess.run([script_path, *args], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            raise RuntimeError(f"Script '{script_name}' in skill '{self.name}' failed with error: {result.stderr}")
        return result.stdout

class SkillsList:
    def __init__(self, skills_dir: Path):
        # Build list of skills
        skills = [Skill(md_file) for md_file in skills_dir.glob("*/SKILL.md") if md_file.exists()]
        self.skills = {
            skill.name: skill for skill in skills if skill.name is not None and skill.description is not None
        }

    def get_skill_descriptions(self) -> str:
        return "\n".join([f"{skill.name}: {skill.description}" for skill in self.skills.values()])
    
    def get_skill(self, skill_name: str) -> Skill | None:
        return self.skills.get(skill_name, None)


if __name__ == "__main__":
    skills_list = SkillsList(Path('/home/teodor/Program/agentti/skills'))

    print(skills_list.get_skill_descriptions())