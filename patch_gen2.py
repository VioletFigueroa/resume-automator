import re

with open('src/generate.py', 'r') as f:
    text = f.read()

# Make sure generator handles custom_cover_letter_body
old_flags = """        context['company_focus'] = role_config.get('company_focus', '')
        context['proximity_note'] = role_config.get('proximity_note', '')"""

new_flags = """        context['company_focus'] = role_config.get('company_focus', '')
        context['proximity_note'] = role_config.get('proximity_note', '')
        context['custom_cover_letter_body'] = role_config.get('custom_cover_letter_body', '')"""

if "context['custom_cover_letter_body']" not in text:
    text = text.replace(old_flags, new_flags)
    with open('src/generate.py', 'w') as f:
        f.write(text)
