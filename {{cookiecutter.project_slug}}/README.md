# {{cookiecutter.project_name.title()}}

Version: 0.1.0

---

## Author(s)

- {{cookiecutter.author}} [[{{cookiecutter.email}}](mailto:{{cookiecutter.email}})]

---

## Description

{{cookiecutter.description}}

---

## Project requirements

- [ ] MkDocs
  - [ ] Home
  - [ ] Design Document
  - [ ] Examples
  - [ ] Performance analysis and profile
  - [ ] API Reference
- [ ] Tests
  - [ ] [Code coverage (-%)](docs/coverage/index.html)
  - [ ] Unit tests
  - [ ] Feature tests
  - [ ] Integration tests
  - [ ] Performance tests
- [ ] Quality Assurance
  - [ ] Code covereage
  - [ ] Code quality
  - [ ] Code style
- [ ] Profiling
  - [ ] Execution time
  - [ ] Memory usage
  - [ ] CPU usage
- [ ] CI/CD 
  - [ ] git actions
  - [ ] Jenkins
- [ ] Demo app
- [ ] Notebooks

---

## Install

With **Pip**:
```bash
pip install git+ssh://git@github.com:/{{cookiecutter.git_username}}/{{cookiecutter.git_reponame}}
```

With **Poetry**:
```bash
poetry add git+ssh://git@github.com:/{{cookiecutter.git_username}}/{{cookiecutter.git_reponame}}
```
