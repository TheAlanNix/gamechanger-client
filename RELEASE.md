# Release Automation Setup

This project includes automated release management that publishes to PyPI when a GitHub release is created.

## Setup Requirements

### 1. PyPI Publishing Setup

This project uses **Trusted Publishing** for secure PyPI authentication. No API tokens needed! ✨

### 2. Repository Permissions
The workflow needs write permissions to update version files. This is automatically granted via the `GITHUB_TOKEN`.

## Version Management

This project uses a dual versioning system:

1. **Semantic versioning** in `pyproject.toml` (e.g., `1.2.3`)
2. **Date-based versioning** in `version.py` (e.g., `2025.10.29`)

## Release Process

### Super Simple Release Process

**Just create the GitHub release**
1. Create a GitHub release with tag `v1.2.3`
2. Done! The workflow handles everything automatically.

That's it! The GitHub release tag is the single source of truth. 🎉

## Workflow Details

The release workflow (`.github/workflows/release.yml`) triggers on:
- GitHub release publication
- Extracts version from release tag (removes 'v' prefix)
- Updates version files
- Builds and publishes to PyPI

## Troubleshooting

### Common Issues

1. **PyPI upload fails**: Check your PyPI token or trusted publishing setup
2. **Version conflicts**: Ensure the tag version doesn't already exist on PyPI
3. **Build failures**: Run `python -m build` locally to test

### Manual PyPI Upload

If automated publishing fails, you can manually upload:

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Version History

The project maintains version history in:
- Git tags for semantic versions
- GitHub releases for release notes
- PyPI for published packages