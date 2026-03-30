import json

with open('private/main_profile.json', 'r') as f:
    data = json.load(f)

for job in data['experience']:
    if job['company'] == 'Self-Employed':
        new_bullet = "Created custom 'How-To' guides for non-technical users to reduce recurring support requests."
        if new_bullet not in job['bullets']:
            job['bullets'].append(new_bullet)

with open('private/main_profile.json', 'w') as f:
    json.dump(data, f, indent=2)

