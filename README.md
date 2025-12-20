# Resume Automator

A Python-based tool to generate tailored resumes and cover letters from a main profile database.

## Features
- **Main Data Source:** Single JSON file (`data/main_profile.json`) containing all career history.
- **Role-Based Tailoring:** JSON configurations define which projects and summaries to use for specific job roles.
- **Automated Generation:** Generates Markdown resumes and cover letters for all configured roles in seconds.
- **PDF Conversion:** Supports converting HTML to PDF using `WeasyPrint` for high-fidelity styling.
- **PII Protection:** Built-in support for separating public template data from private personal information.

## Data Privacy & Security
This project is designed with security in mind to prevent accidental leakage of Personally Identifiable Information (PII) such as phone numbers and email addresses.

- **Public Data (`data/main_profile.json`):** This file is committed to the repository and should only contain placeholder or redacted information (e.g., `email@example.com`).
- **Private Data (`private/main_profile.json`):** The generator looks for this file first. It is added to `.gitignore` by default.
- **Workflow:**
    1. Copy the template: `cp data/main_profile.json private/main_profile.json`
    2. Add your real contact details to the file in `private/`.
    3. Run the generator. It will use your private data for the local files, but your secrets remain safe from `git push`.

## Usage

1.  **Setup:**
    ```bash
    pip install jinja2 weasyprint
    # Note: WeasyPrint requires additional system dependencies (e.g., pango, cairo)
    # On Arch Linux: sudo pacman -S python-weasyprint
    ```

2.  **Personalize:**
    To use your own data without committing it, create a `private/` folder and add your `main_profile.json` there. The script will prioritize this file over the example data.
    ```bash
    mkdir private
    cp data/main_profile.json private/main_profile.json
    # Edit private/main_profile.json with your real details
    ```

3.  **Run:**
    ```bash
    python3 src/generate.py
    ```

4.  **Output:**
    Check the `output/` directory for generated files.

## Directory Structure
- `data/`: Contains example `main_profile.json` and `roles/` configurations.
- `private/`: (Ignored by Git) Place your real `main_profile.json` here.
- `templates/`: Jinja2 templates for resumes and cover letters.
- `src/`: Python source code.
- `output/`: (Ignored by Git) Generated artifacts.

## Author
Violet Figueroa
