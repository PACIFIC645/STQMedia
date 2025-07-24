# Contributing to STQMedia

Thank you for your interest in contributing! We welcome your ideas, code, and suggestions to improve STQMedia.

## Getting Started

1. **Clone the Repository**

    ```bash
    git clone https://github.com/PACIFIC645/STQMedia.git
    cd STQMedia
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment**

    - Copy `.env.example` to `.env` and update variables as needed.

4. **Run Locally**

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Development Environment

This project was developed using [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/). While you can contribute from any system (Linux, macOS, or Windows), **using WSL on Windows is recommended for a smoother setup and compatibility with our tooling and scripts**.

To get started with WSL, see the [official install guide](https://docs.microsoft.com/en-us/windows/wsl/install).

If you encounter environment-specific problems, feel free to ask questions in Issues or Discussions!

## Coding Style

- Use clear, descriptive variable and function names.
- Follow [PEP8](https://pep8.org/) for Python code.
- Use 2 spaces for JavaScript/React, 4 spaces for Python.
- Comment complex logic.
- Keep code modular and DRY (Don’t Repeat Yourself).

## Suggesting Features

- [Open an issue](https://github.com/PACIFIC645/STQMedia/issues/new) with the `enhancement` label.
- Describe the feature, use case, and alternatives considered.

## Issue & PR Etiquette

- Search existing issues/PRs before submitting new ones.
- Use clear, descriptive titles and fill out all templates.
- Reference relevant issues in your PR (e.g., `Closes #issue_number`).
- Write concise commit messages.
- Be respectful in all project interactions.

## Docker Usage (Starter)

- To build and run with Docker:

    ```bash
    docker-compose up --build
    ```

- Environment variables are managed via `.env`.
- See `docker-compose.yml` for service definitions.
- For more, check the project README.

---

Thank you for helping make STQMedia better!
