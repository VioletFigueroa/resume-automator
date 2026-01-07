import json
import os
import subprocess
import argparse
import sys
from datetime import date
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader

# Configuration
DATA_DIR = 'data'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'
PRIVATE_DIR = 'private'

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
            ['weasyprint', html_file, pdf_file], 
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
    summary_key = config.get('summary_type', 'general')
    tailored['summary'] = profile_data['summaries'].get(summary_key, profile_data['summaries']['general'])
    
    # 3. Filter Projects
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

    return tailored

def generate_resume(role_config_path: Optional[str] = None) -> None:
    """
    Generates a resume and cover letter based on the provided role configuration.
    
    Args:
        role_config_path (str, optional): Path to the role configuration JSON file.
    """
    # 1. Load Main Data
    # Check for private data first, otherwise use example data
    private_data_path = os.path.join(PRIVATE_DIR, 'main_profile.json')
    if os.path.exists(private_data_path):
        print(f"Using private data from {private_data_path}")
        profile_data = load_json(private_data_path)
    else:
        print(f"Using example data from {os.path.join(DATA_DIR, 'main_profile.json')}")
        profile_data = load_json(os.path.join(DATA_DIR, 'main_profile.json'))
    
    if not profile_data:
        print("Error: Could not load main profile data. Aborting.")
        return

    # 2. Load Role Config (if provided)
    role_config = {}
    if role_config_path:
        role_config = load_json(role_config_path)
        if not role_config:
             print(f"Error: Could not load role config from {role_config_path}. Skipping.")
             return
    
    # 3. Tailor Data
    context = tailor_data(profile_data, role_config)
    # Include role-specific flags for templates
    if role_config_path:
        context['summary_type'] = role_config.get('summary_type', 'general')
        context['company_focus'] = role_config.get('company_focus', '')
        context['prospective_outreach'] = role_config.get('prospective_outreach', False)
        context['sanitization_standard'] = role_config.get('sanitization_standard', 'NIST 800-88')
    recipient = role_config.get('recipient', {}) if role_config else {}
    context['recipient'] = {
        'name': recipient.get('name', 'Hiring Manager'),
        'title': recipient.get('title', ''),
        'company': recipient.get('company', ''),
        'address': recipient.get('address', ''),
    }
    
    # 4. Render Resume Template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
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
        elif summary_type == 'prs_canada':
            context['background_context'] = "forensic data destruction, chain of custody, and IT asset security"
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
            generate_resume(config_path)
        else:
            print(f"Error: Role configuration file '{args.role}' not found.")
    else:
        # 1. Generate General Resume
        print("--- Generating General Resume ---")
        generate_resume()

        # 2. Generate Tailored Resumes from roles directory
        roles_dir = os.path.join(DATA_DIR, 'roles')
        if os.path.exists(roles_dir):
            print("\n--- Generating Tailored Resumes ---")
            for filename in os.listdir(roles_dir):
                if filename.endswith('.json'):
                    config_path = os.path.join(roles_dir, filename)
                    print(f"Processing: {filename}")
                    generate_resume(config_path)
                    print("-" * 30)

if __name__ == "__main__":
    main()
