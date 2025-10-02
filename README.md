<!-- 
================================================================================
NOTE:
- To use the icon, create an `assets` folder in your project root 
  and place your `treef-logo.png` inside it.
- Replace `rahebsaeed` in the badge URLs below with your actual
  GitHub username.
================================================================================
-->
<div align="center">
  <img src="assets/treef-logo.png" alt="Treef Logo" width="150" height="150">
  <h1>treef</h1>
  <p><strong>Effortlessly scaffold project structures from simple text trees.</strong></p>
  
  <p>
    <!-- PyPI Version -->
    <a href="https://pypi.org/project/treef/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/treef?color=306998&label=pypi%20package"></a>
    <!-- Python Versions -->
    <a href="https://pypi.org/project/treef/"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/treef"></a>
    <!-- License -->
    <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/rahebsaeed/treef?color=blue"></a>
    <!-- Build Status -->
    <a href="https://github.com/rahebsaeed/treef/actions"><img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/rahebsaeed/treef/python-package.yml?branch=main"></a>
    <!-- Test Coverage -->
    <a href="https://codecov.io/gh/rahebsaeed/treef"><img alt="Test Coverage" src="https://img.shields.io/codecov/c/github/rahebsaeed/treef"></a>
  </p>
</div>

Tired of manually creating nested folders and empty files for new projects? **Treef** is a simple, powerful command-line tool that builds a complete directory structure from a single, human-readable `.tree` file.

It's perfect for bootstrapping projects, sharing boilerplate structures, and ensuring consistency across your team.

---

## 🌳 Key Features

*   **Intuitive ASCII Tree Syntax:** Define complex nested structures in a file that looks just like the output of the `tree` command.
*   **Zero Configuration:** Just create a `.tree` file and run a single command.
*   **Interactive Prompt:** If multiple `.tree` files are found, `treef` provides a clean, interactive prompt to choose which one to use.
*   **Safe by Design:** After successfully building the project, the definition file is automatically renamed from `.tree` to `.treef` to prevent accidental re-runs.
*   **Helpful Guidance:** If no `.tree` file is found, `treef` provides a helpful "getting started" guide.
*   **Blazingly Fast:** Written in Python, it's lightweight and executes instantly.

## 🚀 Quick Start

### 1. Installation

Install `treef` from PyPI using pip:

```sh
pip install treef
```

### 2. Create a `.tree` File

In a new, empty project directory, create a file named `my_project.tree`.

```text
# my_project.tree

# A comment describing the project structure.
# Directories are marked with a leading or trailing slash.

/src
    ├── /api
    │   ├── /middleware
    │   └── /routes
    │       ├── auth.routes.js
    │       └── user.routes.js
    ├── /services
    │   └── database.service.js
    ├── app.js
    └── server.js

/tests
    ├── /unit
    └── /integration

.env
.gitignore
package.json
README.md
```

### 3. Run the Command

Navigate to the directory containing your `.tree` file and run:

```sh
treef
```

### 4. See the Result

That's it! Your directory will now be populated with the structure you defined.

**Generated Structure:**
```
.
├── src/
│   ├── api/
│   │   ├── middleware/
│   │   └── routes/
│   │       ├── auth.routes.js
│   │       └── user.routes.js
│   ├── services/
│   │   └── database.service.js
│   ├── app.js
│   └── server.js
├── tests/
│   ├── unit/
│   └── integration/
├── .env
├── .gitignore
├── my_project.treef  <-- Your file was automatically renamed!
├── package.json
└── README.md
```

## ⚙️ Command-Line Options

| Option      | Description                      |
|-------------|----------------------------------|
| `--verbose` | Enable detailed debug logging.   |
| `--help`    | Show the help message and exit.  |


## 🤝 Contributing

Contributions are welcome! If you have a feature request, bug report, or want to improve the code, please feel free to open an issue or submit a pull request.

To set up a development environment:
1.  Clone the repository: `git clone https://github.com/rahebsaeed/treef.git`
2.  Create and activate a virtual environment.
3.  Install in editable mode: `pip install -e .`
4.  Install development dependencies: `pip install -r requirements-dev.txt`
5.  Run tests: `pytest`

## 📜 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.