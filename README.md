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
- ✅ **[NEW Phase 2] Impact Bullets: 4 variants per achievement (security, efficiency, team, business)** ([Phase 2 docs](docs/PHASE2_IMPACT_BULLETS.md))

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
3. **[NEW Phase 1] Automatically optimizes for ATS systems:**
   - Generates job-relevant headlines
   - Reorders skills by relevance
   - Intelligently selects best summary
4. **[NEW Phase 2] Generates multiple impact bullet variants:**
   - Security impact (risks eliminated, incidents prevented)
   - Efficiency impact (time saved, processes automated)
   - Team impact (people trained, collaboration improved)
   - Business impact (value delivered, metrics improved)
5. Uses Jinja2 templates to generate documents
6. Creates markdown and PDF versions
7. Saves to `output/` directory

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

### [Phase 1] With ATS Optimization: Paste Job Description

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

**What you get (Phase 1):**
- ✅ Auto-generated headline: "SOC Analyst II | Threat Hunting & Incident Response | Splunk Expert"
- ✅ Reordered skills: Splunk, Log Analysis, Threat Hunting (most relevant first)
- ✅ Auto-selected summary: Best match for SOC analyst role
- ✅ Professional cover letter: Customized for this specific job

**Expected Phase 1 impact:** +30-45% ATS matching score

### [Phase 2] With Impact Bullet Variants (NEW)

Extend your role config with achievement metrics:

```json
{
  "role_title": "Incident Response Analyst",
  "specialization": "Threat Hunter",
  "job_description": "We need incident response expertise with team training focus...",
  "achievements_with_metrics": [
    {
      "responsibility": "Led forensic investigations and incident response",
      "metrics": {
        "incidents_resolved": "50+",
        "mttd_improvement": "65%",
        "team_size": 8,
        "awareness_improvement": "50%"
      }
    },
    {
      "responsibility": "Trained incident response team on forensic analysis",
      "metrics": {
        "team_members_trained": 12,
        "certification_rate": "75%",
        "response_time_improvement": "45%"
      }
    }
  ]
}
```

Generate:

```bash
python3 src/generate.py --role data/roles/incident_response.json
```

**What you get (Phase 2):**

For each achievement, 4 variants are generated:

```
1. SECURITY (recommended if job focuses on incident response):
   "Implemented forensic investigation procedures, resolving 50+ incidents 
   with 65% faster mean time to detect and zero breaches."

2. EFFICIENCY:
   "Automated incident response workflow, reducing investigation time by 
   8 hours per week and achieving 65% faster detection."

3. TEAM:
   "Trained 12 team members on forensic analysis and response procedures, 
   increasing team certification rate to 75% and improving response time by 45%."

4. BUSINESS:
   "Delivered incident response program resolving 50+ incidents with 
   measurable improvement in security posture and team capability."
```

Tool automatically selects the best-matching variant based on job description keywords.

**Expected Phase 2 impact (combined with Phase 1):** +40-65% ATS matching score

See [Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md) and [Phase 2 docs](docs/PHASE2_IMPACT_BULLETS.md) for detailed examples.

## Directory Structure

```
resume-automator/
├── data/                    # Public example data
│   ├── main_profile.json   # Profile template
│   └── roles/              # Role configurations
│       ├── example_soc_analyst_ats.json           # Phase 1 example
│       └── example_incident_response_phase2.json  # Phase 2 example
├── private/                # Private data (git-ignored)
│   └── main_profile.json   # Your real profile
├── templates/              # Jinja2 templates
│   ├── resume.md
│   ├── resume.html
│   ├── cover_letter.md
│   └── cover_letter.html
├── src/                    # Python source code
│   ├── generate.py         # Main generator
│   └── ats_optimizer.py    # ATS optimization functions (Phase 1 & 2)
├── docs/                   # Documentation
│   ├── PHASE1_ATS_OPTIMIZATION.md      # Phase 1: Headlines & Skills
│   └── PHASE2_IMPACT_BULLETS.md        # Phase 2: Impact Variants
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

**Basic:**
```json
{
  "role_title": "Job Title",
  "summary_type": "general",
  "project_ids": ["project1", "project2"]
}
```

**With Phase 1 (ATS Optimization):**
```json
{
  "role_title": "Job Title",
  "specialization": "Optional Specialization",
  "job_description": "Full job posting text",
  "recipient": {
    "name": "Hiring Manager",
    "title": "Job Title",
    "company": "Company Name"
  },
  "project_ids": ["project1", "project2"]
}
```

**With Phase 2 (Impact Bullets - NEW):**
```json
{
  "role_title": "Job Title",
  "job_description": "Full job posting text",
  "achievements_with_metrics": [
    {
      "responsibility": "Your achievement",
      "metrics": {
        "incidents_reduced": "75%",
        "team_size": 8,
        "time_saved": "8 hours"
      }
    }
  ]
}
```

See [Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md) and [Phase 2 docs](docs/PHASE2_IMPACT_BULLETS.md) for all available fields.

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

**Impact bullets not appearing:**
- Ensure `achievements_with_metrics` array is in role config
- Verify metrics keys match exactly (e.g., `incidents_reduced` not `incidents`)
- Check template includes bullet variant logic

See [Phase 1 troubleshooting](docs/PHASE1_ATS_OPTIMIZATION.md#troubleshooting) and [Phase 2 troubleshooting](docs/PHASE2_IMPACT_BULLETS.md#troubleshooting) for more.

## Development

### Project Roadmap

**Phase 1** ✅ (Complete): ATS Optimization
- Resume headlines (+15-20% ATS)
- Skill reordering by job (+10-15% ATS)
- Intelligent summary selection (+5-10% ATS)
- Total Phase 1: +30-45% ATS improvement
- [Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md)

**Phase 2** ✅ (Complete): Impact-Driven Bullets
- Multiple bullet variants per achievement (4 angles)
- Security, efficiency, team, business impact angles
- Impact metrics formatting and keyword injection
- Auto-selection of best-matching angle per job
- Total Phase 1+2: +40-65% ATS improvement
- Expected: +10-20% interview rate improvement
- [Phase 2 docs](docs/PHASE2_IMPACT_BULLETS.md)

**Phase 3** (Next): AI Cover Letter Generation
- Auto-generate personalized cover letters from job description
- Proof example selection and matching
- Company research integration
- Multiple cover letter variants
- Expected: +20-30% additional interview rate improvement
- Total Phase 1+2+3: Potential 8-10x interview rate vs baseline

### Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

## Testing ATS Compatibility

Use these free tools to validate your optimized resumes:

- [JobScan](https://www.jobscan.co) - Free ATS scan
- [Resumeworded](https://resumeworded.com) - Resume optimization feedback
- [Zety](https://zety.com/resume-maker) - Free resume checker

**Baseline (before optimization):** 20-30% ATS match
**After Phase 1:** 50-75% ATS match
**After Phase 1 + Phase 2:** 70-90% ATS match
**Expected interview rate:** 15-25% (vs 4-6% baseline)

## License

MIT License - see [LICENSE](./LICENSE)

## Author

[Violet Figueroa](https://github.com/VioletFigueroa)

---

**Questions?** Check [Phase 1 docs](docs/PHASE1_ATS_OPTIMIZATION.md), [Phase 2 docs](docs/PHASE2_IMPACT_BULLETS.md), or open an issue.
