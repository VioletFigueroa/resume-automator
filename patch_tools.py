for filename in ['templates/cover_letter.md.j2', 'templates/cover_letter.html.j2']:
    with open(filename, 'r') as f:
        text = f.read()
    
    text = text.replace("skills.tools_platforms", "skills.support_tools_and_platforms")
    
    with open(filename, 'w') as f:
        f.write(text)
