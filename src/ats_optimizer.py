"""ATS Optimization Module

Provides functions to enhance resume quality for ATS systems:
- Resume headline generation
- Skills reordering by relevance
- Keyword extraction from job descriptions
- Impact metrics formatting
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter

# ACTION VERBS FOR RESUME BULLETS
STRONG_ACTION_VERBS = {
    'security': [
        'Implemented', 'Configured', 'Deployed', 'Established', 'Secured',
        'Detected', 'Investigated', 'Analyzed', 'Identified', 'Mitigated',
        'Patched', 'Hardened', 'Monitored', 'Audited', 'Remediated',
        'Eliminated', 'Reduced', 'Prevented', 'Fortified', 'Strengthened'
    ],
    'efficiency': [
        'Automated', 'Streamlined', 'Optimized', 'Accelerated', 'Reduced',
        'Eliminated', 'Decreased', 'Saved', 'Improved', 'Enhanced'
    ],
    'team': [
        'Trained', 'Mentored', 'Led', 'Coordinated', 'Managed', 'Directed',
        'Guided', 'Coached', 'Collaborated', 'Facilitated', 'Supported'
    ],
    'development': [
        'Built', 'Developed', 'Created', 'Designed', 'Engineered',
        'Architected', 'Implemented', 'Deployed', 'Released', 'Launched'
    ]
}

# COMMON JOB KEYWORDS BY DOMAIN
JOB_KEYWORD_MAPPINGS = {
    'soc_analyst': {
        'tools': ['Splunk', 'QRadar', 'ArcSight', 'Sumo Logic', 'ELK Stack'],
        'concepts': ['SIEM', 'threat hunting', 'log analysis', 'incident response', 'threat detection'],
        'frameworks': ['MITRE ATT&CK', 'NIST 800-53', 'CIS Controls']
    },
    'incident_response': {
        'tools': ['Splunk', 'Wireshark', 'Volatility', 'Autopsy', 'Elastic'],
        'concepts': ['forensics', 'incident response', 'breach investigation', 'root cause analysis', 'timeline reconstruction'],
        'frameworks': ['NIST IR', 'SANS IR', 'MITRE ATT&CK']
    },
    'vulnerability_management': {
        'tools': ['Nessus', 'Qualys', 'OpenVAS', 'Rapid7', 'Tenable'],
        'concepts': ['vulnerability assessment', 'vulnerability management', 'risk management', 'patch management', 'CVE analysis'],
        'frameworks': ['CVSS', 'CVRF', 'CIS']
    },
    'appsec': {
        'tools': ['BurpSuite', 'OWASP ZAP', 'Checkmarx', 'SonarQube'],
        'concepts': ['secure code', 'OWASP', 'web security', 'API security', 'secure coding'],
        'frameworks': ['OWASP Top 10', 'CWE', 'SANS Top 25']
    },
    'network_security': {
        'tools': ['Palo Alto', 'Cisco ASA', 'Check Point', 'Fortinet'],
        'concepts': ['network security', 'firewall', 'IDS/IPS', 'VPN', 'network monitoring'],
        'frameworks': ['NIST', 'CIS', 'ISO 27001']
    },
    'cloud_security': {
        'tools': ['AWS Security', 'Azure Security', 'Google Cloud Security', 'CloudTrail'],
        'concepts': ['cloud security', 'infrastructure security', 'cloud compliance', 'identity management'],
        'frameworks': ['CIS Benchmarks', 'Cloud Security Alliance', 'ISO 27001']
    }
}


def extract_job_keywords(job_description: str, domain: str = None) -> Dict[str, List[str]]:
    """
    Extract relevant keywords from a job description.
    
    Args:
        job_description (str): The job posting text
        domain (str): Optional domain hint (e.g., 'soc_analyst', 'incident_response')
    
    Returns:
        dict: Dictionary with 'tools', 'concepts', 'frameworks' keys containing extracted keywords
    """
    job_lower = job_description.lower()
    extracted = {
        'tools': [],
        'concepts': [],
        'frameworks': [],
        'custom': []
    }
    
    # If domain provided, check against known keywords
    if domain and domain in JOB_KEYWORD_MAPPINGS:
        domain_keywords = JOB_KEYWORD_MAPPINGS[domain]
        
        for tool in domain_keywords.get('tools', []):
            if tool.lower() in job_lower:
                extracted['tools'].append(tool)
        
        for concept in domain_keywords.get('concepts', []):
            if concept.lower() in job_lower:
                extracted['concepts'].append(concept)
        
        for framework in domain_keywords.get('frameworks', []):
            if framework.lower() in job_lower:
                extracted['frameworks'].append(framework)
    
    # Extract generic keywords (percentage, years, technologies)
    # Look for years of experience
    years_match = re.findall(r'(\d+)\+?\s+years?', job_lower)
    if years_match:
        extracted['custom'].append(f"{years_match[0]} years")
    
    # Look for specific certifications
    certs = ['Security+', 'CEH', 'CISSP', 'OSCP', 'SANS', 'CompTIA']
    for cert in certs:
        if cert.lower() in job_lower:
            extracted['custom'].append(cert)
    
    return extracted


def generate_resume_headline(
    job_title: str,
    top_skills: List[str],
    specialization: str = None
) -> str:
    """
    Generate a professional, ATS-optimized resume headline.
    
    Format: [Job Title] | [Skill1] & [Skill2] | [Specialization]
    
    Args:
        job_title (str): The target job title
        top_skills (List[str]): Top 2-3 most relevant skills
        specialization (str): Optional specialization (e.g., 'SIEM Expert')
    
    Returns:
        str: A professional resume headline
    
    Example:
        >>> headline = generate_resume_headline(
        ...     'Cybersecurity Analyst',
        ...     ['Incident Response', 'Threat Hunting'],
        ...     'Splunk Expert'
        ... )
        >>> print(headline)
        Cybersecurity Analyst | Incident Response & Threat Hunting | Splunk Expert
    """
    if len(top_skills) >= 2:
        skills_str = ' & '.join(top_skills[:2])
    else:
        skills_str = top_skills[0] if top_skills else 'Security Professional'
    
    if specialization:
        return f"{job_title} | {skills_str} | {specialization}"
    else:
        return f"{job_title} | {skills_str}"


def reorder_skills_by_job(
    all_skills: Dict[str, List[str]],
    job_description: str,
    max_skills: int = 12
) -> List[str]:
    """
    Reorder skills by relevance to a specific job description.
    
    ATS systems scan top-down. This function prioritizes skills that match
    the job posting, up to max_skills (typically 12).
    
    Args:
        all_skills (Dict[str, List[str]]): Categorized skills from profile
        job_description (str): The job posting text
        max_skills (int): Maximum skills to return (default 12)
    
    Returns:
        List[str]: Reordered skills, most relevant first
    
    Example:
        >>> skills = {
        ...     'security_tools': ['Splunk', 'QRadar', 'Wireshark'],
        ...     'programming': ['Python', 'Bash']
        ... }
        >>> job = "We need Splunk SIEM expertise and log analysis"
        >>> reordered = reorder_skills_by_job(skills, job)
        >>> print(reordered[:3])
        ['Splunk', 'Log Analysis', ...]
    """
    job_lower = job_description.lower()
    
    # Flatten all skills
    all_skills_list = []
    for category, skills_list in all_skills.items():
        all_skills_list.extend(skills_list)
    
    # Score each skill based on job description
    scored_skills = []
    for skill in all_skills_list:
        skill_lower = skill.lower()
        score = 0
        
        # Exact phrase match = highest score
        if f'"{skill_lower}"' in job_lower or f' {skill_lower} ' in f' {job_lower} ':
            score += 3
        # Partial match
        elif skill_lower in job_lower:
            score += 2
        # Related keyword match
        else:
            # Check for related keywords
            related_keywords = {
                'Splunk': ['siem', 'log analysis', 'monitoring'],
                'Wireshark': ['packet analysis', 'network traffic', 'protocol'],
                'Python': ['scripting', 'automation', 'programming'],
                'MITRE ATT&CK': ['tactics', 'techniques', 'threat modeling'],
                'NIST 800-53': ['compliance', 'framework', 'controls'],
                'Incident Response': ['ir', 'incident handling', 'response'],
                'Threat Hunting': ['hunting', 'threat detection', 'proactive']
            }
            
            if skill in related_keywords:
                for keyword in related_keywords[skill]:
                    if keyword in job_lower:
                        score += 1
        
        if score > 0:
            scored_skills.append((skill, score))
        else:
            scored_skills.append((skill, 0))
    
    # Sort by score (descending), then alphabetically
    sorted_skills = sorted(scored_skills, key=lambda x: (-x[1], x[0]))
    
    # Return top N skills as strings
    return [skill for skill, score in sorted_skills[:max_skills]]


def generate_impact_bullets(
    responsibility: str,
    metrics: Dict[str, Any] = None,
    impact_type: str = 'security'
) -> List[str]:
    """
    Generate multiple bullet point variants for a single responsibility.
    
    Creates 3-4 variants emphasizing different impact angles:
    - Security impact (for security roles)
    - Efficiency impact (for ops/IT roles)
    - Team/process impact (for leadership roles)
    - Business impact (for executive-facing roles)
    
    Args:
        responsibility (str): The main responsibility/achievement
        metrics (Dict[str, Any]): Optional metrics (percentage, count, time saved, etc.)
        impact_type (str): Primary impact type ('security', 'efficiency', 'team', 'business')
    
    Returns:
        List[str]: 3-4 bullet variants
    
    Example:
        >>> bullets = generate_impact_bullets(
        ...     "Configured firewall and MFA across 30 endpoints",
        ...     {'incidents_reduced': '100%', 'endpoints': 30},
        ...     'security'
        ... )
        >>> for bullet in bullets:
        ...     print(f"- {bullet}")
    """
    metrics = metrics or {}
    variants = []
    
    # Variant 1: Security Impact
    if impact_type == 'security' or 'incidents_reduced' in metrics:
        reduction = metrics.get('incidents_reduced', 'X%')
        endpoints = metrics.get('endpoints', 'all')
        bullet = f"Implemented advanced security controls across {endpoints} endpoints, "
        bullet += f"reducing security incidents by {reduction} and eliminating compromise risks."
        variants.append(bullet)
    
    # Variant 2: Efficiency/Process Impact
    if 'time_saved' in metrics or 'automation_percent' in metrics:
        time = metrics.get('time_saved', 'X hours')
        autom = metrics.get('automation_percent', 'X%')
        bullet = f"Automated security operations across {metrics.get('scope', 'the infrastructure')}, "
        bullet += f"reducing manual work by {time} per week and increasing automation to {autom}."
        variants.append(bullet)
    
    # Variant 3: Team/Training Impact
    if 'team_size' in metrics or 'awareness_improvement' in metrics:
        team = metrics.get('team_size', 'X')
        awareness = metrics.get('awareness_improvement', 'X%')
        bullet = f"Trained {team} team members on security best practices, "
        bullet += f"increasing phishing awareness scores by {awareness} and reducing user-based incidents."
        variants.append(bullet)
    
    # Variant 4: General (always included)
    # Extract first strong action verb and enhance with metrics
    action_verb = next((v for v in STRONG_ACTION_VERBS['security'] if v.lower() in responsibility.lower()), 'Implemented')
    scope = metrics.get('scope', 'across the organization')
    outcome = metrics.get('outcome', 'resulting in measurable security improvements')
    bullet = f"{action_verb} {responsibility}, {outcome}."
    variants.append(bullet)
    
    # Ensure we have at least one variant
    if not variants:
        variants = [responsibility]
    
    return variants


def validate_keyword_density(text: str, keywords: List[str], max_density: float = 0.15) -> Tuple[bool, float]:
    """
    Validate that keyword density doesn't exceed max threshold (avoid keyword stuffing).
    
    Args:
        text (str): The text to check
        keywords (List[str]): Keywords to count
        max_density (float): Maximum allowed keyword density (default 0.15 = 15%)
    
    Returns:
        Tuple[bool, float]: (is_valid, actual_density)
    
    Example:
        >>> text = "Splunk expert analyzing Splunk logs with Splunk SIEM"
        >>> valid, density = validate_keyword_density(text, ['Splunk'])
        >>> print(f"Valid: {valid}, Density: {density:.1%}")
    """
    text_lower = text.lower()
    total_words = len(text_lower.split())
    keyword_count = 0
    
    for keyword in keywords:
        keyword_count += text_lower.count(keyword.lower())
    
    density = keyword_count / total_words if total_words > 0 else 0
    is_valid = density <= max_density
    
    return is_valid, density


def format_metric(value: Any, metric_type: str = 'percentage') -> str:
    """
    Format a metric value for resume display.
    
    Args:
        value (Any): The metric value
        metric_type (str): Type of metric ('percentage', 'count', 'time', 'currency')
    
    Returns:
        str: Formatted metric
    
    Example:
        >>> format_metric(0.40, 'percentage')
        '40%'
        >>> format_metric(12, 'count')
        '12'
        >>> format_metric(8, 'time')
        '8 hours'
    """
    if metric_type == 'percentage':
        if isinstance(value, float):
            return f"{int(value * 100)}%"
        return f"{value}%"
    elif metric_type == 'count':
        return str(value)
    elif metric_type == 'time':
        return f"{value} hours" if isinstance(value, int) else f"{value}"
    elif metric_type == 'currency':
        return f"${value:,.0f}" if isinstance(value, (int, float)) else value
    else:
        return str(value)


def select_best_summary(
    profile_summaries: Dict[str, str],
    job_description: str
) -> Tuple[str, str, float]:
    """
    Intelligently select the best resume summary for a job description.
    
    Scores each available summary against the job description and returns
    the best match.
    
    Args:
        profile_summaries (Dict[str, str]): Available summaries keyed by type
        job_description (str): The job posting text
    
    Returns:
        Tuple[str, str, float]: (summary_key, summary_text, confidence_score)
    
    Example:
        >>> summaries = {
        ...     'general': 'Cybersecurity analyst with 1.5 years...',
        ...     'appsec': 'Full-stack developer with security focus...',
        ...     'soc': 'SIEM specialist with threat hunting expertise...'
        ... }
        >>> job = "Looking for SOC analyst with Splunk and threat hunting"
        >>> key, text, conf = select_best_summary(summaries, job)
        >>> print(f"Best match: {key} (confidence: {conf:.1%})")
    """
    job_lower = job_description.lower()
    scores = {}
    
    for summary_key, summary_text in profile_summaries.items():
        summary_lower = summary_text.lower()
        score = 0
        
        # Check for keyword matches
        keywords = ['splunk', 'siem', 'threat hunting', 'incident response',
                   'appsec', 'web', 'secure', 'application', 'healthcare',
                   'network', 'cloud', 'compliance']
        
        for keyword in keywords:
            if keyword in summary_lower and keyword in job_lower:
                score += 1
        
        # Boost certain summaries for known job types
        if 'soc' in summary_key.lower() and any(x in job_lower for x in ['soc', 'siem', 'monitoring']):
            score += 2
        if 'appsec' in summary_key.lower() and any(x in job_lower for x in ['security', 'developer', 'web', 'api']):
            score += 2
        if 'incident' in job_lower and any(x in summary_key.lower() for x in ['incident', 'response']):
            score += 2
        
        scores[summary_key] = score
    
    # Get best match
    best_key = max(scores, key=scores.get)
    best_score = scores[best_key]
    total_score = sum(scores.values())
    confidence = best_score / total_score if total_score > 0 else 0
    
    return best_key, profile_summaries[best_key], confidence
