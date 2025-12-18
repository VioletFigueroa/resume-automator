# Resume Automator

A Python-based tool to generate tailored resumes and cover letters from a master profile database.

## Features
- **Master Data Source:** Single JSON file (`data/master_profile.json`) containing all career history.
- **Role-Based Tailoring:** JSON configurations define which projects and summaries to use for specific job roles.
- **Automated Generation:** Generates Markdown resumes and cover letters for all configured roles in seconds.
- **PDF Conversion:** Supports converting Markdown to PDF using `pandoc` (requires pandoc installed).

## Usage

1.  **Setup:**
    ```bash
    pip install jinja2
    # Optional: Install pandoc for PDF conversion
    sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra
    ```

2.  **Run:**
    ```bash
    python3 src/generate.py
    ```

3.  **Output:**
    Check the `output/` directory for generated files.

## Directory Structure
- `data/`: Contains `master_profile.json` and `roles/` configurations.
- `templates/`: Jinja2 templates for resumes and cover letters.
- `src/`: Python source code.
- `output/`: Generated artifacts.

## Author
Violet Figueroa
