import json

with open('data/roles/langara_computer_support_technician_JR-4265.json', 'r') as f:
    data = json.load(f)

data['proximity_note'] = "Living just 10 minutes from the main campus, I am highly motivated to contribute to a vital community institution."

# Reorder and simplify skills
data['skills'] = {
    "operating_systems_and_hardware": [
      "Windows 10/11",
      "macOS",
      "Linux (Debian/Kali)",
      "PC/Mac Hardware Troubleshooting",
      "Mobile Devices (iOS/Android)",
      "Printers & Peripherals"
    ],
    "networking": [
      "TCP/IP",
      "Wi-Fi Configuration",
      "LAN/WAN",
      "Routing & Switching",
      "VPN",
      "Network Monitoring",
      "Firewall Rules"
    ],
    "support_tools_and_platforms": [
      "Ticketing Systems",
      "Active Directory",
      "Remote Desktop (RustDesk, RealVNC)",
      "Microsoft 365",
      "WordPress/WooCommerce",
      "GitHub"
    ],
    "security": [
      "Bitwarden",
      "Malwarebytes",
      "Firewalls",
      "Wireshark",
      "Nmap",
      "Endpoint Management"
    ]
}

# Apply experience patches to match Gemini suggestions
with open('private/main_profile.json', 'r') as f:
    main_profile = json.load(f)

experiences = []
for job in main_profile['experience']:
    if job['company'] == 'Shopify':
        continue
    
    if job['company'] == 'Self-Employed':
        job['bullets'].append("Created custom 'How-To' guides for non-technical users to reduce recurring support requests.")

    if job['company'] == 'Compass Group Canada (SFU Dining Hall)':
        job['summary'] = "Worked in a high-volume university environment, interacting daily with a diverse student and faculty population. Navigated unionized workplace structures (UNITE HERE Local 40) directly analogous to Langara's institutional environments."

    experiences.append(job)

data['experience'] = experiences

with open('data/roles/langara_computer_support_technician_JR-4265.json', 'w') as f:
    json.dump(data, f, indent=2)

