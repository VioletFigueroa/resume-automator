import json
import os
import subprocess
from datetime import date
from jinja2 import Environment, FileSystemLoader

# Configuration
DATA_DIR = 'data'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'output'

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def convert_to_pdf(md_file):
    pdf_file = md_file.replace('.md', '.pdf')
    try:
        # Basic pandoc conversion
        # Using -V geometry:margin=1in for better margins
        subprocess.run(['pandoc', md_file, '-o', pdf_file, '-V', 'geometry:margin=1in'], check=True)
        print(f"Generated PDF: {pdf_file}")
    except subprocess.CalledProcessError:
        print(f"Failed to convert {md_file} to PDF. Ensure pandoc is installed.")
    except FileNotFoundError:
        print("Pandoc not found. Skipping PDF conversion.")

def generate_resume(role_config_path=None):
    # 1. Load Master Data
    # Check for private data first, otherwise use example data
    private_data_path = os.path.join('private', 'master_profile.json')
    if os.path.exists(private_data_path):
        print(f"Using private data from {private_data_path}")
        master_data = load_json(private_data_path)
    else:
        print(f"Using example data from {os.path.join(DATA_DIR, 'master_profile.json')}")
        master_data = load_json(os.path.join(DATA_DIR, 'master_profile.json'))
    
    # 2. Load Role Config (if provided)
    role_config = {}
    if role_config_path:
        role_config = load_json(role_config_path)
    
    # 3. Tailor Data
    context = tailor_data(master_data, role_config)
    
    # 4. Render Resume Template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    resume_template = env.get_template('resume.md.j2')
    resume_content = resume_template.render(context)
    
    # 5. Save Resume Output
    role_name = role_config.get('role_title', 'General').replace(' ', '_')
    resume_file = os.path.join(OUTPUT_DIR, f'Resume_{role_name}.md')
    with open(resume_file, 'w') as f:
        f.write(resume_content)
    
    print(f"Generated resume: {resume_file}")
    convert_to_pdf(resume_file)

    # 6. Render Cover Letter Template (if role specific)
    if role_config_path:
        context['date'] = date.today().strftime("%B %d, %Y")
        context['role_title'] = role_config.get('role_title', 'Cyber Security Analyst')
        
        # Determine background context based on summary type
        summary_type = role_config.get('summary_type', 'general')
        if summary_type == 'appsec':
            context['background_context'] = "full-stack development and application security"
        elif summary_type == 'healthcare':
            context['background_context'] = "healthcare compliance and secure system administration"
        else:
            context['background_context'] = "incident response and vulnerability management"

        cl_template = env.get_template('cover_letter.md.j2')
        cl_content = cl_template.render(context)
        
        cl_file = os.path.join(OUTPUT_DIR, f'Cover_Letter_{role_name}.md')
        with open(cl_file, 'w') as f:
            f.write(cl_content)
        print(f"Generated cover letter: {cl_file}")
        convert_to_pdf(cl_file)

def tailor_data(master, config):
    """
    Filters and sorts the master data based on the role configuration.
    """
    tailored = master.copy()
    
    # 1. Set Label/Title
    if 'role_title' in config:
        tailored['basics']['label'] = config['role_title']
        
    # 2. Select Summary
    summary_key = config.get('summary_type', 'general')
    tailored['summary'] = master['summaries'].get(summary_key, master['summaries']['general'])
    
    # 3. Filter Projects
    # Combine all projects into a flat list for easier filtering
    all_projects = master['projects']['cyber'] + master['projects']['web'] + master['projects']['personal']
    
    if 'project_ids' in config:
        # Filter by ID and preserve order defined in config
        tailored['projects'] = [p for pid in config['project_ids'] for p in all_projects if p.get('id') == pid]
    else:
        # Default: Show top 5 cyber projects
        tailored['projects'] = master['projects']['cyber'][:5]

    # 4. Reorder Skills (Optional - simple implementation)
    # Could be expanded to filter specific skills
    
    return tailored

if __name__ == "__main__":
    # 1. Generate General Resume
    print("Generating General Resume...")
    generate_resume()

    # 2. Generate Tailored Resumes from roles directory
    roles_dir = os.path.join(DATA_DIR, 'roles')
    if os.path.exists(roles_dir):
        for filename in os.listdir(roles_dir):
            if filename.endswith('.json'):
                config_path = os.path.join(roles_dir, filename)
                print(f"Generating resume for config: {filename}...")
                generate_resume(config_path)
