"""
Project Scaffolder for Pixel Readme Kit v4.0
Generates initial README.template.md from predefined templates:
- study: Laboratory reports and academic work
- library: Open Source libraries and packages
- cli: Command-line utilities and system tools
"""

import os
import re

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

def get_available_templates():
    return ["study", "library", "cli"]

def scaffold_readme(
    project_type="library",
    title="MY PROJECT",
    subtitle=None,
    author="DEVELOPER",
    group="SE-01",
    discipline="COMPUTER SCIENCE",
    repo=None,
    output_path="README.template.md"
) -> str:
    """
    Creates a customized README.template.md from a built-in template.
    """
    ptype = project_type.lower()
    tpl_filename = f"{ptype}.template.md"
    tpl_path = os.path.join(TEMPLATE_DIR, tpl_filename)

    if not os.path.exists(tpl_path):
        raise ValueError(f"Unknown template type '{project_type}'. Available: {get_available_templates()}")

    with open(tpl_path, "r", encoding="utf-8") as f:
        content = f.read()

    slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', title.lower()).strip('-') or "my-project"
    repo_val = repo if repo else f"username/{slug}"
    sub_val = subtitle if subtitle else f"{title.upper()} // SYSTEM ARCHITECTURE"

    replacements = {
        "{PROJECT_TITLE}": title,
        "{PROJECT_SUBTITLE}": sub_val,
        "{PROJECT_SLUG}": slug,
        "{AUTHOR}": author,
        "{GROUP}": group,
        "{DISCIPLINE}": discipline,
        "{REPO}": repo_val,
    }

    for key, val in replacements.items():
        content = content.replace(key, str(val))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path
