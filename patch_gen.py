import re

with open('src/generate.py', 'r') as f:
    text = f.read()

# Add logic to override skills and experience
old_filter_exp = """    if 'exclude_companies' in config and isinstance(profile_data.get('experience'), list):"""

new_filter_exp = """    # 2.5 Override or Filter Experience
    if 'experience' in config:
        tailored['experience'] = config['experience']
        print(f"  Using custom experience list from config.")
    elif 'exclude_companies' in config and isinstance(profile_data.get('experience'), list):"""

text = text.replace(old_filter_exp, new_filter_exp)

old_reorder = """    # 3. Reorder Skills by Job"""
new_reorder = """    # 3. Reorder Skills by Job
    if 'skills' in config:
        tailored['skills'] = config['skills']
        print(f"  Using custom skills list from config.")"""
text = text.replace(old_reorder, new_reorder)

old_flags = """    if role_config_path:
        context['summary_type'] = role_config.get('summary_type', 'general')
        context['company_focus'] = role_config.get('company_focus', '')"""

new_flags = """    if role_config_path:
        context['summary_type'] = role_config.get('summary_type', 'general')
        context['company_focus'] = role_config.get('company_focus', '')
        context['proximity_note'] = role_config.get('proximity_note', '')"""

text = text.replace(old_flags, new_flags)

with open('src/generate.py', 'w') as f:
    f.write(text)
