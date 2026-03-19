for filename in ['templates/cover_letter.md.j2', 'templates/cover_letter.html.j2']:
    with open(filename, 'r') as f:
        text = f.read()
    
    if '{% if custom_cover_letter_body %}' not in text:
        marker = "Dear {{ recipient.name }},"
        start_idx = text.find(marker) + len(marker) + 1
        end_idx = text.find("Sincerely,")
        
        replacement = """
{% if custom_cover_letter_body %}
{{ custom_cover_letter_body }}
{% else %}
""" + text[start_idx:end_idx] + """
{% endif %}
"""
        new_text = text[:start_idx] + replacement + text[end_idx:]
        
        with open(filename, 'w') as f:
            f.write(new_text)

import json
with open('data/roles/langara_computer_support_technician_JR-4265.json', 'r') as f:
    data = json.load(f)

data['custom_cover_letter_body'] = """
I am writing to express my strong interest in the Computer Support Technician position at Langara College. Living less than a 10-minute walk from the main campus, I have long admired Langara’s role as a vital community institution. I am eager to bring my decade of technical troubleshooting, system administration, and client-centered customer service experience to your IT department to help keep students, faculty, and staff productive during critical academic periods.

Throughout my career, I have developed a strong foundation in providing patient, empathetic support across diverse environments. As a Freelance IT Support Technician and the primary IT resource for Accessible Places, I honed my ability to resolve hardware, software, and network issues across Windows, macOS, and Linux systems. I pride myself on translating complex technical concepts into clear, accessible language for users of all technical backgrounds. Furthermore, my time working at Simon Fraser University provided me with deep experience navigating a high-volume, unionized academic environment, equipping me with the institutional awareness necessary to thrive at Langara.

Technically, I am well-prepared to handle the dynamic demands of a college service desk. My CompTIA Security+ certification ensures that I approach endpoint management, access controls, and network troubleshooting with a security-first mindset. Beyond basic troubleshooting, I actively leverage Python and Bash scripting to automate routine maintenance tasks, and I frequently create comprehensive user documentation to reduce recurring support requests.

I am highly motivated to contribute my technical expertise and user-focused approach to the Langara community. I would welcome the opportunity to discuss how my skills align with your team's needs. Thank you for your time and consideration.
"""

with open('data/roles/langara_computer_support_technician_JR-4265.json', 'w') as f:
    json.dump(data, f, indent=2)

