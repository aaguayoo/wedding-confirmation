"""Generate dependencies documentation."""

# Usar 'toml' si tu Python es <3.11
import toml  # type: ignore


def extract_dependencies(pyproject_path: str = "pyproject.toml") -> dict:
    """Extracts dependencies from a pyproject.toml configuration file.

    This function reads and parses a pyproject.toml file to retrieve project
    dependencies and development dependencies. It supports both Poetry-based and
    PEP 621 standard project configurations.

    Args:
        pyproject_path (str, optional):
            Path to the pyproject.toml file. Defaults to "pyproject.toml".

    Returns:
        dict: A dict containing three dictionaries - project dependencies,
        development dependencies and documentation dependencies.

    """
    with open(pyproject_path, "r") as file:
        data = toml.load(file)

    # Para proyectos basados en Poetry
    dependencies = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    dev_dependencies = (
        data.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("dev", {})
        .get("dependencies", {})
    )
    doc_dependencies = (
        data.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("doc", {})
        .get("dependencies", {})
    )
    api_dependencies = (
        data.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("api", {})
        .get("dependencies", {})
    )
    prod_dependencies = (
        data.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("prod", {})
        .get("dependencies", {})
    )

    # Si usas el estándar PEP 621
    # dependencies = data.get("project", {}).get("dependencies", [])

    return {
        "main": dependencies,
        "dev": dev_dependencies,
        "doc": doc_dependencies,
        "api": api_dependencies,
        "prod": prod_dependencies,
    }


def generate_dependencies_doc(output_path: str = "docs/dependencies.md") -> None:
    """Generates a markdown documentation file listing project dependencies.

    This function retrieves project dependencies and writes them to a markdown file,
    organizing dependencies into main and development categories.

    Args:
        output_path (str, optional):
            File path where the dependencies documentation will be written.
            Defaults to "docs/dependencies.md".

    """
    deps = extract_dependencies()

    with open(output_path, "w") as file:
        file.write("# Project Dependencies\n\n")

        file.write("## Main Dependencies\n")
        for dep, version in deps["main"].items():
            file.write(f"- **{dep}**: {version}\n")

        file.write("\n## Development Dependencies\n")
        for dep, version in deps["dev"].items():
            file.write(f"- **{dep}**: {version}\n")

        file.write("\n## Documentation Dependencies\n")
        for dep, version in deps["doc"].items():
            file.write(f"- **{dep}**: {version}\n")

        file.write("\n## API Dependencies\n")
        for dep, version in deps["api"].items():
            file.write(f"- **{dep}**: {version}\n")

        file.write("\n## Production Dependencies\n")
        for dep, version in deps["prod"].items():
            file.write(f"- **{dep}**: {version}\n")


if __name__ == "__main__":
    generate_dependencies_doc()
