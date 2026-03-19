with open('templates/cover_letter.html.j2', 'r') as f:
    text = f.read()
old = "Your commitment to {{ company_focus or 'client-centered IT support' }} aligns with my experience providing practical troubleshooting, clear communication, and user-focused technical support in fast-moving environments."
new = "Your commitment to {{ company_focus or 'client-centered IT support' }} aligns with my experience providing practical troubleshooting, clear communication, and user-focused technical support in fast-moving environments. {% if proximity_note %} {{ proximity_note }}{% endif %}"
with open('templates/cover_letter.html.j2', 'w') as f:
    f.write(text.replace(old, new))
