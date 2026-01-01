# Documentation

Complete documentation for Resume Automator.

## Getting Started

- **Setup Guide** - Installation and configuration
- **Usage Examples** - How to generate resumes and cover letters

## Reference

- **Project Structure** - Directory organization
- **Data Format** - Profile JSON schema
- **Security** - PII protection best practices

## Quick Start

```bash
# 1. Install dependencies
pip install jinja2 weasyprint

# 2. Setup private data folder
mkdir private
cp data/main_profile.json private/main_profile.json

# 3. Edit your data
# Edit private/main_profile.json with your real details

# 4. Generate
python3 src/generate.py

# 5. Find output
# Check output/ directory
```

## Files in This Folder

- **README.md** - Documentation index (this file)

## Main Documentation

See main [../README.md](../README.md) for full project overview.

---

**Last updated:** 2025-01-01
