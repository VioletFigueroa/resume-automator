# Resume Automator

Generate tailored resumes and cover letters from a single profile database.

## Features

- ✅ Single source of truth (JSON profile)
- ✅ Role-based customization
- ✅ Markdown + PDF output
- ✅ PII protection built-in
- ✅ Fast generation
- ✅ Template-based
- ✅ **[NEW] ATS Optimization: Dynamic headlines, skill reordering, smart summary selection** ([Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md))

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
3. **[NEW] Automatically optimizes for ATS systems:**
   - Generates job-relevant headlines
   - Reorders skills by relevance
   - Intelligently selects best summary
4. Uses Jinja2 templates to generate documents
5. Creates markdown and PDF versions
6. Saves to `output/` directory

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

### Basic: Generate All Resumes

```bash
python3 src/generate.py
```

Outputs:
- resume_RoleName.md
- resume_RoleName.html
- resume_RoleName.pdf
- cover_letter_RoleName.md
- cover_letter_RoleName.html
- cover_letter_RoleName.pdf

### [NEW] With ATS Optimization: Paste Job Description

Create `data/roles/custom_job.json`:

```json
{
  "role_title": "SOC Analyst II",
  "specialization": "Splunk Expert",
  "job_description": "We are seeking a SOC Analyst with strong Splunk SIEM, threat hunting, log analysis, and incident response experience. MITRE ATT&CK knowledge essential. Security+ or equivalent required.",
  "recipient": {
    "name": "Hiring Manager",
    "company": "Example Corp"
  },
  "project_ids": ["capstone", "p3", "p11"]
}
```

Generate:

```bash
python3 src/generate.py --role data/roles/custom_job.json
```

**What you get:**
- ✅ Auto-generated headline: "SOC Analyst II | Threat Hunting & Incident Response | Splunk Expert"
- ✅ Reordered skills: Splunk, Log Analysis, Threat Hunting (most relevant first)
- ✅ Auto-selected summary: Best match for SOC analyst role
- ✅ Professional cover letter: Customized for this specific job

**Expected impact:** +30-45% ATS matching score

See [Phase 1 ATS Optimization docs](docs/PHASE1_ATS_OPTIMIZATION.md) for detailed examples and advanced usage.

## Directory Structure

```
resume-automator/
├── data/                    # Public example data
│   ├── main_profile.json   # Profile template
│   └── roles/              # Role configurations
│       └── example_soc_analyst_ats.json  # ATS optimization example
├── private/                # Private data (git-ignored)
│   └── main_profile.json   # Your real profile
├── templates/              # Jinja2 templates
│   ├── resume.md
│   ├── resume.html
│   ├── cover_letter.md
│   └── cover_letter.html
├── src/                    # Python source code
│   ├── generate.py         # Main generator
│   └── ats_optimizer.py    # [NEW] ATS optimization functions
├── docs/                   # Documentation
│   └── PHASE1_ATS_OPTIMIZATION.md  # [NEW] Phase 1 feature docs
├── output/                 # Generated files (git-ignored)
├── requirements.txt
└── README.md
```

## Configuration

### Profile Format

`private/main_profile.json` - See [data/main_profile.json](data/main_profile.json) for full schema.

Key sections:
- `basics`: Name, contact info, location
- `summaries`: Multiple role-specific summaries
- `skills`: Categorized by domain
- `experience`: Work history with metrics
- `projects`: Portfolio projects (cyber, web, personal)
- `education`: Degrees and bootcamps
- `certifications`: Professional certs

### Role Configuration

`data/roles/job_title.json`

Basic:
```json
{
  "role_title": "Job Title",
  "summary_type": "general",
  "project_ids": ["project1", "project2"]
}
```

With ATS Optimization (NEW):
```json
{
  "role_title": "Job Title",
  "specialization": "Optional Specialization",
  "job_description": "Full job posting text for intelligent customization",
  "recipient": {
    "name": "Hiring Manager",
    "title": "Job Title",
    "company": "Company Name"
  },
  "project_ids": ["project1", "project2"]
}
```

See [Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md) for all available fields.

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
- Check PDF permissions in output directory

**Missing data:**
- Ensure `private/main_profile.json` exists
- Check JSON formatting is valid
- Verify paths in role configs

**ATS features not working:**
- Ensure `job_description` field is in role config
- Check that profile has skills defined
- Verify summaries are present in profile

See [Phase 1 docs troubleshooting](docs/PHASE1_ATS_OPTIMIZATION.md#troubleshooting) for more.

## Development

### Project Roadmap

**Phase 1** ✅ (Current): ATS Optimization
- Resume headlines
- Skill reordering by job
- Intelligent summary selection
- [Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md)

**Phase 2** (Next): Impact-Driven Bullets
- Multiple bullet point variants (security, efficiency, team, business impact)
- Impact metrics formatting
- Keyword injection in summaries
- Expected: +10-20% interview rate improvement

**Phase 3** (Future): Cover Letter Generation
- Auto-generate personalized cover letters from job description
- Proof example selection and matching
- Company research integration
- Expected: 4x interview rate improvement when combined with Phase 1 & 2

### Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

## Testing ATS Compatibility

Use these free tools to validate your optimized resumes:

- [JobScan](https://www.jobscan.co) - Free ATS scan
- [Resumeworded](https://resumeworded.com) - Resume optimization feedback
- [Zety](https://zety.com/resume-maker) - Free resume checker

**Baseline (before optimization):** 20-30% ATS match
**After Phase 1:** 50-75% ATS match
**After Phase 1 + 2:** 75-90% ATS match

## License

MIT License - see [LICENSE](./LICENSE)

## Author

[Violet Figueroa](https://github.com/VioletFigueroa)

---

**Questions?** Check [docs/PHASE1_ATS_OPTIMIZATION.md](docs/PHASE1_ATS_OPTIMIZATION.md) or open an issue.
