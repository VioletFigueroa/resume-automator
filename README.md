# Resume Automator

Generate tailored resumes and cover letters from a single profile database.

## Features

- ✅ Single source of truth (JSON profile)
- ✅ Role-based customization
- ✅ Markdown + PDF output
- ✅ PII protection built-in
- ✅ Fast generation
- ✅ Template-based

## Quick Start

```bash
# 1. Install dependencies
pip install jinja2 weasyprint

# 2. Setup private data
mkdir private
cp data/main_profile.json private/main_profile.json

# 3. Edit with your details
# Edit private/main_profile.json

# 4. Generate
python3 src/generate.py

# 5. Find outputs
# Check output/ directory
```

## How It Works

1. Loads your profile from `private/main_profile.json`
2. Reads role configurations from `data/roles/`
3. Uses Jinja2 templates to generate documents
4. Creates markdown and PDF versions
5. Saves to `output/` directory

## Security

- **Public Data** (`data/`): Example/placeholder data only
- **Private Data** (`private/`): Your real information (git-ignored)
- **Workflow**: Tool uses private data locally, keeps secrets safe

## Installation

### Prerequisites

- Python 3.8+
- WeasyPrint (requires system dependencies)

### Setup

```bash
# Clone
git clone https://github.com/VioletFigueroa/resume-automator.git
cd resume-automator

# Install
pip install -r requirements.txt

# Configure
mkdir private
cp data/main_profile.json private/main_profile.json
# Edit private/main_profile.json with your real details
```

## Usage

```bash
# Generate all configured resumes
python3 src/generate.py

# Output files
# resume_RoleName.md
# resume_RoleName.html
# cover_letter_RoleName.md
# cover_letter_RoleName.html
```

## Directory Structure

```
resume-automator/
├── data/                    # Public example data
│   ├── main_profile.json   # Profile template
│   └── roles/              # Role configurations
├── private/                # Private data (git-ignored)
│   └── main_profile.json   # Your real profile
├── templates/              # Jinja2 templates
│   ├── resume.md
│   ├── resume.html
│   ├── cover_letter.md
│   └── cover_letter.html
├── src/                    # Python source code
│   ├── generate.py         # Main generator
│   └── ...
├── output/                 # Generated files (git-ignored)
└── README.md
```

## Configuration

### Profile Format

`data/main_profile.json`:

```json
{
  "name": "Your Name",
  "email": "your@example.com",
  "phone": "+1-555-0000",
  "experience": [
    {
      "title": "Role Title",
      "company": "Company",
      "period": "2020-2023",
      "description": "What you did"
    }
  ],
  "skills": ["Python", "JavaScript", ...]
}
```

### Role Configuration

`data/roles/job_title.json`:

```json
{
  "name": "Job Title",
  "include_projects": ["project1", "project2"],
  "include_summaries": ["summary1"],
  "highlight_skills": ["python", "devops"]
}
```

## PDF Generation

WeasyPrint requires system dependencies:

```bash
# macOS
brew install python-weasyprint

# Ubuntu/Debian
sudo apt install python3-weasyprint

# Arch
sudo pacman -S python-weasyprint
```

## Troubleshooting

**PDF generation fails:**

- Install WeasyPrint system dependencies
- Check PDF permission in output directory

**Missing data:**

- Ensure `private/main_profile.json` exists
- Check JSON formatting is valid
- Verify paths in role configs

**Generation is slow:**

- PDF generation takes time
- Use dry-run mode to skip PDF

## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](./LICENSE)

## Author

[Violet Figueroa](https://github.com/VioletFigueroa)

---

**Questions?** Check [docs/](./docs/) or open an issue.
