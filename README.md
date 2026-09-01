# Code Refactoring and Object-Oriented Programming

This repository is a hands-on learning path for writing cleaner Python code. It focuses on refactoring, core OOP concepts, and practical data validation with Pydantic.

## Learning Objectives

By the end of this repository, you should be able to:

- Refactor variables and functions for readability and maintainability.
- Apply OOP concepts (classes, objects, encapsulation, inheritance) in Python.
- Build and validate structured data models with Pydantic.

## Learning Path

| File / Folder | Description |
|---|---|
| [**01 - Refactoring Variables**](01-refactoring-variables.ipynb) | Variable refactoring through exercises on intent-revealing names, pronounceable naming, consistent vocabulary, and removing magic values. Also covers DRY, avoiding mental mapping, and using explanatory variables. |
| [**02 - Refactoring Functions**](02-refactoring-functions.ipynb) | Function refactoring by extracting reusable helpers, keeping functions focused on one task, and working at a single level of abstraction. Also introduces clearer naming, type hints, avoiding side effects, default arguments, removing boolean flags, and reducing parameter count. |
| [**03 - Object-Oriented Programming**](03-object-oriented-programming.ipynb) | Core OOP concepts including classes, objects, attributes, initializers, and methods. Also covers encapsulation with getters and setters, inheritance, and overridden methods. |
| [**04 - Pydantic**](04-pydantic.ipynb) | Practical introduction to Pydantic for data validation with typed models, covering type coercion, `ValidationError`, field and constrained types, strict types, and custom validators in Pydantic v2. |

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**assets**](assets/) | Visual aids referenced in the notebooks. |
| [**data**](data/) | Dataset used across the notebooks. |
| [**pyproject.toml**](pyproject.toml) | Project configuration and dependencies. |
| [**uv.lock**](uv.lock) | Dependency lock file. |

## Setup

> [!NOTE]
> Throughout these steps, text in angle brackets like `<repo-name>` is a **placeholder**. Replace it, including the `< >` brackets, with your own value. For example, `cd <repo-name>` becomes `cd my-refactoring-project`.

### 1. Create the Repository from the Template

Click **Use this template** on GitHub.

When creating the repository:

- Set yourself as the **Owner**
- Choose a repository name
- Disable **Include all branches**
- Click **Create repository**

> [!IMPORTANT]
> If you are working in pairs or groups, only **one person** should complete this step.

---

### 2. Add Collaborators (Pairs/Groups Only)

If working with teammates:

1. Open the repository on GitHub
2. Go to **Settings → Collaborators**
3. Add your teammates as collaborators
4. Share the repository link with your team

Teammates should accept the invitation before continuing.

---

### 3. Clone the Repository

Copy the SSH URL from the **Code** button on GitHub, then run:

```bash
git clone <copied-ssh-url>
```

The copied SSH URL will look like `git@github.com:<your-username>/<repo-name>.git`.

---

### 4. Move into the Project Folder and Install Dependencies

This installs all dependencies and creates a virtual environment in `.venv/`.

```bash
cd <repo-name>
uv sync
```

---

### 5. Open the Notebooks

> [!NOTE]
> Make sure you open VS Code from the project root so it automatically detects the environment created by `uv sync`.

Launch VS Code in the project root folder:

```bash
code .
```

Then open a notebook and select the Python environment created by `uv sync` as the kernel.

## References & Further Reading

- [**Refactoring.Guru**](https://refactoring.guru/refactoring): A comprehensive guide to code smells and refactoring techniques.
- [**Classes (Python Tutorial)**](https://docs.python.org/3/tutorial/classes.html): The official Python tutorial chapter on classes and OOP.
- [**Pydantic**](https://docs.pydantic.dev/latest/): Official docs for the Pydantic data validation library.
