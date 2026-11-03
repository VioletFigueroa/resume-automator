import json
import os
import subprocess
import argparse
import sys
from datetime import date
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
from ats_optimizer import (
    generate_resume_headline,
    reorder_skills_by_job,
    extract_job_keywords,
    select_best_summary
)

# Configuration
DATA_DIR = 'data'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
PRIVATE_DIR = 'private'
PHONE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'phonenumber.env'))

def load_json(filepath: str) -> Dict[str, Any]:
    """
    Loads JSON data from a file.
    
    Args:
        filepath (str): Path to the JSON file.
        
    Returns:
        dict: The loaded JSON data, or an empty dict if loading fails.
    """
    if not os.path.exists(filepath):
        print(f"Warning: File not found at {filepath}")
        return {}
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return {}
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return {}

def load_phone_number(filepath: str = PHONE_FILE) -> str:
    """Load a phone number from a raw value or PHONE_NUMBER= entry."""
    if not os.path.exists(filepath):
        return ''
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                value = line.strip()
                if not value or value.startswith('#'):
                    continue
                if '=' in value:
                    key, value = value.split('=', 1)
                    if key.strip().lower() not in {'phone', 'phone_number', 'phonenumber'}:
                        continue
                return value.strip().strip('"\'')
    except OSError as error:
        print(f"Warning: Could not read phone number file: {error}")
    return ''

def resume_bullet(value: str) -> str:
    """Keep resume bullets in the coursework-required point-form style."""
    return value.rstrip().rstrip('.;:')

def normalize_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add compatibility aliases for the current main profile schema."""
    basics = profile_data.get('basics', {})
    basics.setdefault('linkedin', basics.get('linkedin_url', ''))
    basics.setdefault('github', basics.get('github_url', ''))
    basics.setdefault('portfolio', basics.get('portfolio_url', ''))
    phone_number = load_phone_number()
    if phone_number:
        basics['phone'] = phone_number
    profile_data['basics'] = basics

    for education in profile_data.get('education', []):
        if education.get('bullets'):
            continue
        bullets = []
        if education.get('resume_bullet'):
            bullets.append(education['resume_bullet'])
        elif education.get('credential_status'):
            bullets.append(education['credential_status'])
        elif education.get('course_code_correction'):
            bullets.append(education['course_code_correction'])
        education['bullets'] = bullets

    return profile_data

def normalize_role_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Support nested target configs while retaining the legacy renderer contract."""
    if 'resume' not in config and 'cover_letter' not in config:
        return config

    resume = config.get('resume', {})
    cover_letter = config.get('cover_letter', {})
    normalized = dict(config)
    normalized.update({
        'role_title': 'Software Developer Intern',
        'output_label': 'IBM C3 EXPE 2300',
        'headline': 'Software Development | Python, JavaScript, React, Node.js',
        'summary_type': 'general',
        'exclude_companies': ['Shopify', 'Compass Group Canada (SFU Dining Hall)'],
        'targeted_resume': True,
        'project_ids': [
            'tinyapp', 'tweeter', 'lightbnb', 'scheduler', 'scheduler-api',
            'lotide', 'resume-automator', 'conversation-to-logseq',
            'perplexport', 'homelab'
        ],
        'recipient': {
            'name': 'Hiring Committee',
            'company': 'IBM Canada Ltd.',
            'address': cover_letter.get('employer_address', '')
        },
        'background_context': 'full-stack software development and security-first engineering',
        'cover_letter_template': 'cover_letter.md.j2',
        'cover_letter_html_template': 'cover_letter.html.j2'
    })

    highlights = resume.get('highlights_order_mirrors_posting', [])
    normalized['job_description'] = ' '.join(highlights)
    normalized['highlights_order_mirrors_posting'] = highlights
    normalized['cover_letter_context'] = cover_letter.get('paragraph_plan', [])
    normalized['custom_cover_letter_body'] = (
        "I am writing to express my interest in the Software Developer Intern pipeline "
        "opportunity with IBM Canada Ltd., identified through the Langara C3 job board.\n\n"
        "As a current Langara College Computer Studies student, I am "
        "building on coursework in web development and programming with hands-on projects "
        "using Python, JavaScript, React, Node.js, Express, PostgreSQL, SQL, REST APIs, "
        "and Git. My academic work includes a URL shortener, a React scheduling application, "
        "a database-backed rental platform, and a JavaScript utility library built from scratch.\n\n"
        "I also bring a security-first perspective through CompTIA Security+ certification, "
        "documented testing, and practical software and automation projects published on GitHub. "
        "My Debian and Docker Compose homelab gives me a concrete environment for developing "
        "cloud and container skills, while my cybersecurity training has strengthened my "
        "analytical thinking and attention to reliable implementation.\n\n"
        "I am available for a full 12-16 month work term and would welcome consideration for "
        "IBM's Software Developer Intern pipeline. Thank you for your time and consideration."
    )
    normalized['role_config_source'] = {
        'resume': resume,
        'cover_letter': cover_letter
    }
    return normalized

def convert_to_pdf(html_file: str) -> None:
    """
    Converts an HTML file to PDF using WeasyPrint.
    
    Args:
        html_file (str): Path to the HTML file.
    """
    pdf_file = html_file.replace('.html', '.pdf')
    try:
        # Use WeasyPrint via command line
        subprocess.run(
            [sys.executable, '-m', 'weasyprint', html_file, pdf_file],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        print(f"  [PDF] Generated: {pdf_file}")
    except subprocess.CalledProcessError as e:
        print(f"  [PDF] Failed to convert {html_file}. Error: {e}")
    except FileNotFoundError:
        print("  [PDF] WeasyPrint not found. Skipping PDF conversion.")

def tailor_data(profile_data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filters and sorts the profile data based on the role configuration.
    
    Args:
        profile_data (dict): The main profile data.
        config (dict): The role-specific configuration.
        
    Returns:
        dict: A new dictionary with tailored data.
    """
    tailored = profile_data.copy()
    
    # 1. Set Label/Title
    if 'role_title' in config:
        tailored['basics']['label'] = config['role_title']
        
    # 2. Select Summary
    # Priority order: summary_text (verbatim override) > summary_type (explicit key) > auto-select from job_description > 'general'
    if 'summary_text' in config:
        # Fully custom summary provided directly in the role config
        tailored['summary'] = config['summary_text']
        tailored['summary_key'] = 'custom'
        print(f"  Using custom summary_text from role config.")
    elif 'summary_type' in config:
        summary_key = config['summary_type']
        tailored['summary'] = profile_data['summaries'].get(summary_key, profile_data['summaries']['general'])
        tailored['summary_key'] = summary_key
        print(f"  Using explicit summary: {summary_key}")
    elif 'job_description' in config:
        # Auto-select based on job description when no explicit type given
        summary_key, selected_summary, confidence = select_best_summary(
            profile_data['summaries'],
            config['job_description']
        )
        tailored['summary'] = selected_summary
        tailored['summary_key'] = summary_key
        tailored['summary_confidence'] = confidence
        print(f"  Auto-selected summary: {summary_key} (confidence: {confidence:.1%})")
    else:
        summary_key = 'general'
        tailored['summary'] = profile_data['summaries'].get(summary_key, profile_data['summaries']['general'])
        tailored['summary_key'] = summary_key

    # 2.5 Optional Experience Filtering
    # Allows role-specific omission of employers (e.g., sensitive or non-targeted short tenures)
    # 2.5 Override or Filter Experience
    if 'experience' in config:
        tailored['experience'] = config['experience']
        print(f"  Using custom experience list from config.")
    elif 'exclude_companies' in config and isinstance(profile_data.get('experience'), list):
        exclude_set = {
            company.strip().lower()
            for company in config.get('exclude_companies', [])
            if isinstance(company, str) and company.strip()
        }
        if exclude_set:
            original_count = len(profile_data['experience'])
            tailored['experience'] = [
                job for job in profile_data['experience']
                if job.get('company', '').strip().lower() not in exclude_set
            ]
            filtered_count = len(tailored['experience'])
            if filtered_count != original_count:
                print(f"  Filtered experience entries: {original_count - filtered_count} excluded by company rule.")
    
    # 3. Reorder Skills by Job
    if 'skills' in config:
        tailored['skills'] = config['skills']
        print(f"  Using custom skills list from config.")
    if 'job_description' in config:
        print(f"  Reordering skills based on job description...")
        reordered_skills = reorder_skills_by_job(
            tailored['skills'],
            config['job_description'],
            max_skills=12
        )
        # Keep skills as a dict, but create a reordered version for alternate display
        tailored['skills_reordered'] = reordered_skills
        # For template compatibility, keep the original categorized format
        # but we can use skills_reordered in templates if needed
    
    # 4. Generate Resume Headline
    # If headline is explicitly set in the role config, use it verbatim.
    # Otherwise, auto-generate from the job description and top reordered skills.
    if 'headline' in config:
        tailored['headline'] = config['headline']
        print(f"  Using explicit headline: {config['headline']}")
    elif 'job_description' in config:
        role_title = config.get('role_title', 'Cybersecurity Professional')
        # Use top 2-3 reordered skills for headline
        top_skills = tailored.get('skills_reordered', [])[:3]
        if not top_skills:
            top_skills = list(profile_data['skills'].get('security_tools', []))[:3]
        
        headline = generate_resume_headline(
            role_title,
            top_skills,
            specialization=config.get('specialization', None)
        )
        tailored['headline'] = headline
        print(f"  Generated headline: {headline}")
    
    # 5. Filter Projects
    # Combine all projects into a flat list for easier filtering
    all_projects = (
        profile_data['projects'].get('cyber', []) + 
        profile_data['projects'].get('web', []) + 
        profile_data['projects'].get('personal', [])
    )
    
    if 'project_ids' in config:
        # Filter by ID and preserve order defined in config
        tailored['projects'] = [
            p for pid in config['project_ids'] 
            for p in all_projects if p.get('id') == pid
        ]
    else:
        # Default: Show top 5 cyber projects if no config provided
        tailored['projects'] = profile_data['projects'].get('cyber', [])[:5]

    selected_ids = {project.get('id') for project in tailored.get('projects', [])}
    tailored['academic_projects'] = [
        project for project in profile_data['projects'].get('web', [])
        if not selected_ids or project.get('id') in selected_ids
    ]
    tailored['personal_projects'] = [
        project for project in profile_data['projects'].get('personal', [])
        if not selected_ids or project.get('id') in selected_ids
    ]
    tailored['highlights'] = config.get('highlights_order_mirrors_posting', [])
    volunteer_experience = profile_data.get('volunteer_experience', [])
    tailored['volunteer_experience'] = (
        volunteer_experience if isinstance(volunteer_experience, list)
        else [volunteer_experience] if volunteer_experience else []
    )

    if config.get('targeted_resume'):
        tailored['education'] = profile_data.get('education', [])[:2]
        tailored['skills'] = {
            'programming': profile_data.get('skills', {}).get('programming', [])[:12],
            'web_and_apis': ['React', 'Node.js', 'Express', 'PostgreSQL', 'REST/JSON APIs'],
            'development_tools': ['Git', 'GitHub', 'Docker Compose', 'Linux/Debian', 'Jest', 'Cypress'],
            'security_and_systems': ['Secure coding', 'Input validation', 'Authentication', 'Parameterized queries']
        }

    return tailored

def generate_resume(role_config_path: Optional[str] = None, profile_path: Optional[str] = None) -> None:
    """
    Generates a resume and cover letter based on the provided role configuration.
    
    Args:
        role_config_path (str, optional): Path to the role configuration JSON file.
    """
    # 1. Load Main Data
    # Check for private data first, otherwise use example data
    private_data_path = profile_path or os.path.join(PRIVATE_DIR, 'main_profile.json')
    if os.path.exists(private_data_path):
        print(f"Using private data from {private_data_path}")
        profile_data = load_json(private_data_path)
    else:
        print(f"Using example data from {os.path.join(DATA_DIR, 'main_profile.template.json')}")
        profile_data = load_json(os.path.join(DATA_DIR, 'main_profile.template.json'))
    
    if not profile_data:
        print("Error: Could not load main profile data. Aborting.")
        return
    profile_data = normalize_profile(profile_data)

    # 2. Load Role Config (if provided)
    role_config = {}
    if role_config_path:
        role_config = load_json(role_config_path)
        if not role_config:
             print(f"Error: Could not load role config from {role_config_path}. Skipping.")
             return
        role_config = normalize_role_config(role_config)
    
    # 3. Tailor Data
    context = tailor_data(profile_data, role_config)
    # Include role-specific flags for templates
    if role_config_path:
        context['summary_type'] = role_config.get('summary_type', 'general')
        context['company_focus'] = role_config.get('company_focus', '')
        context['proximity_note'] = role_config.get('proximity_note', '')
        context['custom_cover_letter_body'] = role_config.get('custom_cover_letter_body', '')
        context['prospective_outreach'] = role_config.get('prospective_outreach', False)
        context['sanitization_standard'] = role_config.get('sanitization_standard', 'NIST 800-88')
        context['posting_title'] = role_config.get('posting_title')
        context['reference_number'] = role_config.get('reference_number')
        context['interest_points'] = role_config.get('interest_points', [])
        context['requirements'] = role_config.get('requirements', [])
        context['assets'] = role_config.get('assets', [])
        context['organization_mission'] = role_config.get('organization_mission')
        context['output_label'] = role_config.get('output_label')
        public_sector = context.get('public_sector', {}).copy()
        public_sector_overrides = role_config.get('public_sector_overrides', {})
        if public_sector_overrides:
            public_sector.update(public_sector_overrides)
            context['public_sector'] = public_sector
    recipient = role_config.get('recipient', {}) if role_config else {}
    context['recipient'] = {
        'name': recipient.get('name', 'Hiring Manager'),
        'title': recipient.get('title', ''),
        'company': recipient.get('company', ''),
        'address': recipient.get('address', ''),
    }
    
    # 4. Render Resume Template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    env.filters['resume_bullet'] = resume_bullet
    try:
        # Markdown
        resume_template = env.get_template('resume.md.j2')
        resume_content = resume_template.render(context)
        
        # HTML
        html_template = env.get_template('resume.html.j2')
        html_content = html_template.render(context)
    except Exception as e:
        print(f"Error rendering resume template: {e}")
        return
    
    # 5. Save Resume Output
    candidate_name = context['basics']['name']
    role_title = context['basics']['label']
    output_label = context.get('output_label')
    if output_label:
        base_filename_resume = f"{candidate_name} - {role_title} - {output_label} - Resume"
    else:
        base_filename_resume = f"{candidate_name} - {role_title} - Resume"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    resume_file = os.path.join(OUTPUT_DIR, f'{base_filename_resume}.md')
    with open(resume_file, 'w', encoding='utf-8') as f:
        f.write(resume_content)
    
    html_file = os.path.join(OUTPUT_DIR, f'{base_filename_resume}.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated Resume: {resume_file}")
    print(f"Generated HTML Resume: {html_file}")
    convert_to_pdf(html_file)

    # 6. Render Cover Letter Template (if role specific)
    if role_config_path:
        context['date'] = date.today().strftime("%B %d, %Y")
        context['role_title'] = role_config.get('role_title', 'Cyber Security Analyst')
        
        # Add cover_letter_context to template context if present
        if 'cover_letter_context' in role_config:
            context['cover_letter_context'] = role_config['cover_letter_context']
        
        # Determine background context based on summary type
        summary_type = role_config.get('summary_type', 'general')
        if summary_type == 'appsec':
            context['background_context'] = "full-stack development and application security"
        elif summary_type == 'healthcare':
            context['background_context'] = "healthcare compliance and secure system administration"
        elif summary_type == 'it_support':
            context['background_context'] = "IT service desk support, endpoint troubleshooting, and user training across Windows/macOS/Linux environments"
        elif summary_type == 'prs_canada':
            context['background_context'] = "forensic data destruction, chain of custody, and IT asset security"
        elif summary_type == 'ymca_network_security':
            context['background_context'] = "network security operations, SIEM monitoring, and incident response"
        else:
            context['background_context'] = "incident response and vulnerability management"

        try:
            # Allow custom template selection from role config
            cl_template_name = role_config.get('cover_letter_template', 'cover_letter.md.j2')
            cl_template = env.get_template(cl_template_name)
            cl_content = cl_template.render(context)
            
            cl_html_template_name = role_config.get('cover_letter_html_template', 'cover_letter.html.j2')
            cl_html_template = env.get_template(cl_html_template_name)
            cl_html_content = cl_html_template.render(context)
            
            if output_label:
                base_filename_cl = f"{candidate_name} - {role_title} - {output_label} - Cover Letter"
            else:
                base_filename_cl = f"{candidate_name} - {role_title} - Cover Letter"
            
            cl_file = os.path.join(OUTPUT_DIR, f'{base_filename_cl}.md')
            with open(cl_file, 'w', encoding='utf-8') as f:
                f.write(cl_content)
                
            cl_html_file = os.path.join(OUTPUT_DIR, f'{base_filename_cl}.html')
            with open(cl_html_file, 'w', encoding='utf-8') as f:
                f.write(cl_html_content)
                
            print(f"Generated Cover Letter: {cl_file}")
            print(f"Generated HTML Cover Letter: {cl_html_file}")
            convert_to_pdf(cl_html_file)
        except Exception as e:
            print(f"Error rendering cover letter template: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate tailored resumes and cover letters.")
    parser.add_argument('--role', help="Generate for a specific role configuration file (e.g., 'soc_analyst.json').")
    parser.add_argument('--profile', help="Path to the main profile JSON file.")
    args = parser.parse_args()

    if args.role:
        # Generate for specific role
        # Check if the user provided a full path or just a filename
        if os.path.exists(args.role):
            config_path = args.role
        else:
            config_path = os.path.join(DATA_DIR, 'roles', args.role)
            
        if os.path.exists(config_path):
            print(f"Generating resume for config: {config_path}...")
            generate_resume(config_path, args.profile)
        else:
            print(f"Error: Role configuration file '{args.role}' not found.")
    else:
        # 1. Generate General Resume
        print("--- Generating General Resume ---")
        generate_resume(profile_path=args.profile)

        # 2. Generate Tailored Resumes from roles directory
        roles_dir = os.path.join(DATA_DIR, 'roles')
        if os.path.exists(roles_dir):
            print("\n--- Generating Tailored Resumes ---")
            for filename in os.listdir(roles_dir):
                if filename.endswith('.json'):
                    config_path = os.path.join(roles_dir, filename)
                    print(f"Processing: {filename}")
                    generate_resume(config_path, args.profile)
                    print("-" * 30)

if __name__ == "__main__":
    main()
