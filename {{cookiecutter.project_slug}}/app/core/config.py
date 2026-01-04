"""{{cookiecutter.project_name.title()}} API config."""


class Settings:
    """API settings."""

    APP_NAME: str = "{{cookiecutter.project_name.title()}} API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "{{cookiecutter.description}}"


settings = Settings()
