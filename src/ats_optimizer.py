"""ATS Optimization Module

Provides functions to enhance resume quality for ATS systems:
- Resume headline generation
- Skills reordering by relevance
- Keyword extraction from job descriptions
- Impact metrics formatting
- Impact bullet variants (Phase 2)
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter

# ACTION VERBS FOR RESUME BULLETS - ORGANIZED BY IMPACT TYPE
ACTION_VERBS_BY_IMPACT = {
    'security': [
        'Implemented', 'Configured', 'Deployed', 'Established', 'Secured',
        'Detected', 'Investigated', 'Analyzed', 'Identified', 'Mitigated',
        'Patched', 'Hardened', 'Monitored', 'Audited', 'Remediated',
        'Eliminated', 'Reduced', 'Prevented', 'Fortified', 'Strengthened',
        'Responded', 'Contained', 'Closed', 'Isolated', 'Resolved'
    ],
    'efficiency': [
        'Automated', 'Streamlined', 'Optimized', 'Accelerated', 'Reduced',
        'Eliminated', 'Decreased', 'Saved', 'Improved', 'Enhanced',
        'Scaled', 'Maximized', 'Minimized', 'Simplified', 'Consolidated'
    ],
    'team': [
        'Trained', 'Mentored', 'Led', 'Coordinated', 'Managed', 'Directed',
        'Guided', 'Coached', 'Collaborated', 'Facilitated', 'Supported',
        'Organized', 'Developed', 'Established', 'Built', 'Fostered'
    ],
    'business': [
        'Increased', 'Enhanced', 'Improved', 'Boosted', 'Maximized',
        'Achieved', 'Surpassed', 'Delivered', 'Generated', 'Captured',
        'Reduced', 'Saved', 'Cut', 'Decreased', 'Minimized'
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

# IMPACT ANGLE TEMPLATES
IMPACT_TEMPLATES = {
    'security': {
        'template': "Implemented {responsibility} across {scope}, reducing security incidents by {metric} and {outcome}.",
        'keywords': ['secure', 'incident', 'threat', 'vulnerability', 'protection', 'detection', 'response'],
        'verbs': ACTION_VERBS_BY_IMPACT['security'][:5]
    },
    'efficiency': {
        'template': "Automated {responsibility} across {scope}, reducing manual work by {metric} and increasing efficiency by {outcome}.",
        'keywords': ['automated', 'streamlined', 'optimized', 'faster', 'improved', 'reduced'],
        'verbs': ACTION_VERBS_BY_IMPACT['efficiency'][:5]
    },
    'team': {
        'template': "Trained {num_people} team members on {responsibility}, increasing awareness by {metric} and {outcome}.",
        'keywords': ['trained', 'team', 'people', 'collaboration', 'knowledge', 'culture'],
        'verbs': ACTION_VERBS_BY_IMPACT['team'][:5]
    },
    'business': {
        'template': "Delivered {responsibility} achieving {metric} improvement in {outcome} and business value.",
        'keywords': ['achieved', 'delivered', 'generated', 'increased', 'improved', 'value'],
        'verbs': ACTION_VERBS_BY_IMPACT['business'][:5]
    }
}


def _is_quantifiable_metric(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str) and re.search(r"\d", value):
        return True
    return False


def _format_generic_metric(value: Any) -> str:
    if isinstance(value, float):
        if 0 < value < 1:
            return f"{int(value * 100)}%"
        if value.is_integer():
            return str(int(value))
        return str(value)
    if isinstance(value, int):
        return str(value)
    return str(value)


def extract_quantifiable_metrics(metrics: Dict[str, Any]) -> List[Tuple[str, str]]:
    prioritized_keys = [
        'incidents_reduced', 'risks_mitigated', 'vulnerabilities',
        'time_saved', 'hours_saved', 'automation_percent',
        'team_size', 'people_trained',
        'cost_savings', 'revenue', 'value', 'roi'
    ]

    results: List[Tuple[str, str]] = []
    for key in prioritized_keys:
        if key in metrics and _is_quantifiable_metric(metrics[key]):
            results.append((key, _format_generic_metric(metrics[key])))

    for key, value in metrics.items():
        if key in prioritized_keys:
            continue
        if _is_quantifiable_metric(value):
            results.append((key, _format_generic_metric(value)))

    return results


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


def generate_impact_variants(
    responsibility: str,
    metrics: Dict[str, Any] = None,
    job_description: str = None,
    context: str = None
) -> Dict[str, Any]:
    """
    Generate multiple bullet point variants with different impact angles.
    
    NEW IN PHASE 2: Creates 3-4 variants emphasizing:
    - Security impact (risks eliminated, incidents prevented)
    - Efficiency impact (time saved, processes automated)
    - Team impact (people trained, collaboration improved)
    - Business impact (value delivered, metrics improved)
    
    Args:
        responsibility (str): The main responsibility/achievement
        metrics (Dict[str, Any]): Optional metrics (percentage, count, time, etc.)
        job_description (str): Optional job posting for keyword matching
        context (str): Optional additional context
    
    Returns:
        Dict[str, Any]: Contains 'variants' list and 'scores' for each angle
    
    Example:
        >>> impact = generate_impact_variants(
        ...     "Configured firewall and MFA across 30 endpoints",
        ...     {'incidents_reduced': '100%', 'endpoints': 30, 'team_size': 30},
        ...     "SOC analyst role with security focus"
        ... )
        >>> for angle, bullet in impact['variants'].items():
        ...     print(f"{angle}: {bullet}")
    """
    metrics = metrics or {}
    job_lower = (job_description or '').lower()
    quantifiable_metrics = extract_quantifiable_metrics(metrics)
    fallback_metric = quantifiable_metrics[0][1] if quantifiable_metrics else 'X%'

    def pick_metric(keys: List[str], default_value: str) -> str:
        for key in keys:
            if key in metrics and _is_quantifiable_metric(metrics[key]):
                return _format_generic_metric(metrics[key])
        return default_value
    
    # Determine which angles are most relevant
    angles_to_generate = ['security', 'efficiency', 'team', 'business']
    
    variants = {}
    scores = {}
    
    # SECURITY ANGLE
    if 'incidents' in metrics or 'risks' in metrics or 'vulnerabilities' in metrics or 'incident' in job_lower:
        incidents = pick_metric(
            ['incidents_reduced', 'risks_mitigated', 'vulnerabilities'],
            fallback_metric
        )
        scope = metrics.get('scope', metrics.get('endpoints', 'systems'))
        verb = ACTION_VERBS_BY_IMPACT['security'][0]
        bullet = f"{verb} {responsibility} affecting {scope}, reducing security incidents by {incidents}."
        variants['security'] = bullet
        scores['security'] = 1.0 if 'incident' in job_lower else 0.8
    
    # EFFICIENCY ANGLE
    if 'time_saved' in metrics or 'automated' in job_lower or 'automation' in responsibility.lower():
        time_saved = pick_metric(
            ['time_saved', 'hours_saved', 'time_reduced'],
            fallback_metric
        )
        scope = metrics.get('scope', 'operations')
        percent = pick_metric(
            ['automation_percent', 'efficiency_gain'],
            fallback_metric
        )
        verb = ACTION_VERBS_BY_IMPACT['efficiency'][0]
        bullet = f"{verb} {responsibility} across {scope}, reducing manual work by {time_saved} per week."
        variants['efficiency'] = bullet
        scores['efficiency'] = 1.0 if 'automated' in job_lower or 'streamline' in job_lower else 0.7
    
    # TEAM IMPACT ANGLE
    if 'team_size' in metrics or 'people_trained' in metrics or 'trained' in responsibility.lower():
        team = pick_metric(['team_size', 'people_trained'], 'X')
        awareness = pick_metric(['awareness_improvement', 'knowledge_gain'], fallback_metric)
        topic = context or responsibility.split()[2:] if len(responsibility.split()) > 2 else 'security practices'
        verb = ACTION_VERBS_BY_IMPACT['team'][0]
        bullet = f"{verb} {team} team members on {responsibility}, increasing awareness by {awareness}."
        variants['team'] = bullet
        scores['team'] = 1.0 if 'team' in job_lower or 'trained' in job_lower else 0.6
    
    # BUSINESS/VALUE ANGLE
    if any(k in metrics for k in ['cost_savings', 'revenue', 'value', 'roi']):
        value = pick_metric(['cost_savings', 'revenue', 'value', 'roi'], fallback_metric)
        outcome = metrics.get('outcome', 'business value')
        verb = ACTION_VERBS_BY_IMPACT['business'][0]
        bullet = f"{verb} {responsibility}, delivering {value} in {outcome}."
        variants['business'] = bullet
        scores['business'] = 1.0
    
    # Always include a general impact variant
    if not variants:
        verb = ACTION_VERBS_BY_IMPACT['security'][0]
        metric_str = ' (' + ', '.join([f"{k}: {v}" for k, v in metrics.items()][:2]) + ')' if metrics else ''
        bullet = f"{verb} {responsibility}{metric_str}."
        variants['general'] = bullet
        scores['general'] = 0.5
    
    return {
        'variants': variants,
        'scores': scores,
        'recommended': max(scores, key=scores.get) if scores else 'general',
        'count': len(variants)
    }


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

    # Domain-specific signal keywords mapped to expected summary keys
    SUMMARY_SIGNALS = {
        'appsec': [
            'application security', 'appsec', 'secure sdlc', 'sast', 'dast',
            'secure code review', 'web application', 'api security', 'owasp',
            'developer', 'software engineer', 'full[- ]stack'
        ],
        'ymca_network_security': [
            'siem', 'soc', 'threat hunting', 'incident response',
            'vulnerability management', 'network monitoring', 'endpoint',
            'firewall', 'ids', 'ips', 'wireshark', 'splunk', 'qradar',
            'enterprise environment', 'security operations', 'nist',
            'cloud security', 'iam', 'identity', 'patch management',
            'supply chain', 'third.party risk', 'data loss prevention',
            'digital forensics', 'threat intelligence'
        ],
        'healthcare': [
            'healthcare', 'hipaa', 'pipeda', 'epic', 'ehr', 'clinical',
            'hospital', 'medical', 'health information'
        ],
        'prs_canada': [
            'data destruction', 'data sanitization', 'chain of custody',
            'asset disposal', 'nist 800.88', 'dod 5220', 'recycling', 'refurbishment'
        ],
        'general': [
            'government', 'public sector', 'federal', 'crown', 'agency',
            'compliance', 'governance', 'risk', 'audit', 'policy', 'regulatory'
        ],
        'it_support': [
            'it support', 'helpdesk', 'help desk', 'desktop support',
            'service desk', 'level 1', 'level 2', 'tier 1', 'tier 2',
            'end user', 'hardware', 'troubleshooting', 'technical support'
        ],
    }

    import re as _re

    for summary_key, summary_text in profile_summaries.items():
        summary_lower = summary_text.lower()
        score = 0.0

        # Score based on which domain's signals appear in the job description
        for sig_key, signals in SUMMARY_SIGNALS.items():
            for signal in signals:
                # Use regex for flexibility (handles phrases and optional hyphens)
                if _re.search(signal, job_lower):
                    if sig_key == summary_key:
                        # Job description mentions this summary's domain directly
                        score += 2.0
                    # Cross-penalise: if the signal matches a different domain
                    # strongly, reduce the score for other summaries slightly
                    break  # count each signal group once per summary_key pass

        # Also score by how many job-description keywords appear in the summary itself
        broad_keywords = [
            'splunk', 'siem', 'threat hunting', 'incident response',
            'vulnerability', 'network', 'cloud', 'compliance', 'nist',
            'iam', 'identity', 'endpoint', 'monitoring', 'forensic',
            'government', 'federal', 'enterprise', 'secure', 'firewall'
        ]
        for kw in broad_keywords:
            if kw in summary_lower and kw in job_lower:
                score += 0.5

        scores[summary_key] = score

    # Get best match
    best_key = max(scores, key=scores.get)
    best_score = scores[best_key]
    total_score = sum(scores.values())
    confidence = best_score / total_score if total_score > 0 else 0

    return best_key, profile_summaries[best_key], confidence
