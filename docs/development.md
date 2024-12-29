# Development

## Contributing

If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request. I don't have a formal code of conduct or contribution guidelines yet, but I appreciate respectful and constructive contributions.

## CI/CD Process

### Continuous Integration (CI)

The CI workflow is defined in `.github/workflows/ci.yml`. It runs on every push to any branch and performs the following steps runs all tests using pytest. 

### Continuous Deployment (CD)

The CD workflow is defined in `.github/workflows/cd.yml`. It triggers when the CI workflow completes successfully on the `main` or `dev` branches and performs the following steps builds the package (with Flit), releases to pypi (test pypi for dev, prod pypi for main), and creates a GitHub release.

### Version Bumping

Before committing to release a new version, manually bump the version number in the local `pyproject.toml` file to the target version.
