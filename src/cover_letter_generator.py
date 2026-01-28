"""Cover Letter Generation Module

Provides AI-powered cover letter generation from job descriptions:
- Automatic opening paragraph generation
- Achievement-to-requirement matching
- Professional closing paragraph
- Multiple variant generation
- Company research integration
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# OPENING TEMPLATES
OPENING_TEMPLATES = {
    'enthusiastic': "I am excited to apply for the {job_title} position at {company_name}. With my {years}+ years of experience in {primary_skill} and proven track record in {domain}, I am confident I can make immediate contributions to your team.",
    
    'direct': "As a {primary_skill} professional with {years}+ years of hands-on experience in {domain}, I am writing to express my strong interest in the {job_title} role at {company_name}.",
    
    'achievement': "Your search for a {job_title} who can {key_responsibility} aligns perfectly with my background. I have successfully led {achievement_count}+ initiatives in {domain}, delivering measurable results that directly support {company_benefit}.",
    
    'cultural': "I am drawn to {company_name}'s commitment to {company_value}, and I believe my expertise in {primary_skill} and passion for {domain} make me an ideal candidate for the {job_title} position."
}

# BODY SECTION TEMPLATES
BODY_TEMPLATES = {
    'achievement': "In my current role, I {achievement_verb} {achievement_detail}, resulting in {achievement_result}. This experience has equipped me with the {key_skill} skills needed to {job_requirement}.",
    
    'collaboration': "I have consistently collaborated with cross-functional teams to {collaboration_detail}, improving {improvement_metric} by {improvement_percent}. This background aligns with your need for someone who can {job_need}.",
    
    'technical': "My expertise spans {skill_list}, enabling me to {technical_capability}. I am particularly interested in your team's work on {company_initiative}, where I can contribute through my proficiency in {relevant_skill}.",
    
    'impact': "Throughout my career, I have focused on {impact_area}, and my contributions have resulted in {quantified_impact}. I am excited to bring this track record of {success_type} to {company_name}."
}

# CLOSING TEMPLATES
CLOSING_TEMPLATES = {
    'enthusiastic': "I am excited about the opportunity to contribute to {company_name}'s mission and would welcome the chance to discuss how my background in {primary_skill} can support your team's goals. Thank you for considering my application.",
    
    'professional': "I appreciate your consideration and would be pleased to discuss how my experience in {domain} can benefit {company_name}. I look forward to the opportunity to speak with you.",
    
    'action': "I am confident that my skills in {primary_skill} and commitment to {company_value} make me a strong fit for this role. I am available for an interview at your earliest convenience and can be reached at {contact_info}.",
    
    'partnership': "I believe my background in {domain} positions me well to contribute meaningfully to {company_name}'s objectives. I look forward to discussing this exciting opportunity with you."
}

# COMPANY VALUES & BENEFITS KEYWORDS
COMPANY_KEYWORDS = {
    'innovation': ['cutting-edge', 'advanced', 'emerging', 'next-generation', 'forward-thinking'],
    'security': ['protecting', 'safeguarding', 'defending', 'securing', 'resilience'],
    'efficiency': ['streamlining', 'optimizing', 'automating', 'improving', 'accelerating'],
    'teamwork': ['collaborating', 'partnering', 'coordinating', 'supporting', 'enabling'],
    'growth': ['scaling', 'expanding', 'developing', 'strengthening', 'building'],
    'quality': ['excellence', 'precision', 'reliability', 'standards', 'excellence']
}


def extract_company_info(job_description: str) -> Dict[str, str]:
    """
    Extract company name and key information from job posting.
    
    Args:
        job_description (str): The job posting text
    
    Returns:
        Dict[str, str]: Extracted company information
    
    Example:
        >>> job = "Join Acme Corp as a Security Analyst..."
        >>> info = extract_company_info(job)
        >>> print(info['company_name'])
        'Acme Corp'
    """
    info = {
        'company_name': 'the company',
        'company_size': 'mid-size',
        'industry': 'technology',
        'location': 'remote',
        'founded': '2010',
        'values': []
    }
    
    job_lower = job_description.lower()
    
    # Extract company name (usually first capitalized phrase)
    company_match = re.search(r'(?:join|company|we are|we\'re)\s+([A-Z][A-Za-z\s&]+?)(?:\.|,|at)', job_description)
    if company_match:
        info['company_name'] = company_match.group(1).strip()
    
    # Detect company size
    if any(word in job_lower for word in ['startup', 'early-stage', '<50 employees']):
        info['company_size'] = 'startup'
    elif any(word in job_lower for word in ['enterprise', 'fortune 500', '5000+']):
        info['company_size'] = 'enterprise'
    elif any(word in job_lower for word in ['mid-size', 'scale-up', '100-500']):
        info['company_size'] = 'mid-size'
    
    # Detect industry
    industries = {
        'security': ['security', 'cybersecurity', 'infosec'],
        'fintech': ['financial', 'banking', 'payments'],
        'healthcare': ['healthcare', 'medical', 'pharma'],
        'cloud': ['cloud', 'aws', 'azure', 'gcp'],
        'enterprise': ['enterprise', 'b2b', 'saas']
    }
    for ind, keywords in industries.items():
        if any(kw in job_lower for kw in keywords):
            info['industry'] = ind
            break
    
    # Detect location
    if 'remote' in job_lower:
        info['location'] = 'remote'
    elif any(city in job_description for city in ['New York', 'San Francisco', 'London', 'Toronto']):
        info['location'] = re.search(r'(New York|San Francisco|London|Toronto|Seattle|Austin)', job_description).group(1)
    
    # Extract company values
    values_patterns = [
        r'we value\s+([^.]+)',
        r'our values?\s+include\s+([^.]+)',
        r'committed to\s+([^.]+)'
    ]
    for pattern in values_patterns:
        match = re.search(pattern, job_lower)
        if match:
            values_text = match.group(1)
            for value_set, keywords in COMPANY_KEYWORDS.items():
                if any(kw in values_text for kw in keywords):
                    info['values'].append(value_set)
    
    return info


def select_proof_examples(
    achievements: List[Dict[str, Any]],
    job_requirements: List[str],
    top_n: int = 2
) -> List[Tuple[str, str, float]]:
    """
    Select best achievement examples to support job requirements.
    
    Args:
        achievements (List[Dict]): List of achievements from profile
        job_requirements (List[str]): Required skills/experiences from job
        top_n (int): Number of top matches to return
    
    Returns:
        List[Tuple[str, str, float]]: (requirement, achievement, match_score)
    
    Example:
        >>> achievements = [
        ...     {'description': 'Led incident response for 50+ incidents'},
        ...     {'description': 'Trained 12 analysts on forensics'}
        ... ]
        >>> reqs = ['incident response', 'team training']
        >>> matches = select_proof_examples(achievements, reqs)
        >>> for req, ach, score in matches:
        ...     print(f"{req}: {score:.0%}")
    """
    if not achievements or not job_requirements:
        return []
    
    matches = []
    
    for requirement in job_requirements:
        requirement_lower = requirement.lower()
        best_score = 0
        best_achievement = None
        
        for achievement in achievements:
            achievement_text = achievement.get('description', '').lower()
            if not achievement_text:
                continue
            
            # Calculate match score
            score = 0
            
            # Exact phrase match
            if requirement_lower in achievement_text:
                score += 3
            # Partial keyword match
            else:
                words = requirement_lower.split()
                matching_words = sum(1 for word in words if word in achievement_text)
                score += matching_words
            
            # Boost for metrics/numbers
            if re.search(r'\d+%|\d+\+|\$\d+', achievement_text):
                score += 0.5
            
            if score > best_score:
                best_score = score
                best_achievement = achievement_text
        
        if best_achievement:
            match_confidence = min(best_score / 5, 1.0)  # Normalize to 0-1
            matches.append((requirement, best_achievement, match_confidence))
    
    # Sort by confidence and return top N
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches[:top_n]


def generate_cover_letter_opening(
    job_title: str,
    company_name: str,
    years_experience: int,
    primary_skill: str,
    domain: str,
    style: str = 'enthusiastic',
    company_info: Dict[str, Any] = None
) -> str:
    """
    Generate opening paragraph for cover letter.
    
    Args:
        job_title (str): Target job title
        company_name (str): Company name
        years_experience (int): Years in field
        primary_skill (str): Primary skill/expertise
        domain (str): Domain (e.g., 'SOC operations', 'incident response')
        style (str): Style of opening ('enthusiastic', 'direct', 'achievement', 'cultural')
        company_info (Dict): Optional company information
    
    Returns:
        str: Opening paragraph
    
    Example:
        >>> opening = generate_cover_letter_opening(
        ...     job_title='SOC Analyst II',
        ...     company_name='SecureCorp',
        ...     years_experience=3,
        ...     primary_skill='SIEM',
        ...     domain='threat detection'
        ... )
    """
    company_info = company_info or extract_company_info('')
    company_value = company_info.get('values', ['excellence'])[0] if company_info.get('values') else 'excellence'
    company_benefit = f"your {company_info.get('industry', 'technology')} mission"
    
    template = OPENING_TEMPLATES.get(style, OPENING_TEMPLATES['enthusiastic'])
    
    opening = template.format(
        job_title=job_title,
        company_name=company_name,
        years=years_experience,
        primary_skill=primary_skill,
        domain=domain,
        key_responsibility='detect and respond to security threats',
        achievement_count=50,
        company_benefit=company_benefit,
        company_value=company_value
    )
    
    return opening


def generate_cover_letter_body(
    achievements: List[Dict[str, Any]],
    job_requirements: List[str],
    company_name: str,
    style: str = 'achievement'
) -> str:
    """
    Generate body paragraph(s) for cover letter.
    
    Args:
        achievements (List[Dict]): Key achievements from profile
        job_requirements (List[str]): Job requirements to address
        company_name (str): Company name
        style (str): Style of body content
    
    Returns:
        str: Body paragraph(s)
    
    Example:
        >>> achievements = [
        ...     {'description': 'Led 50+ incident response investigations'}
        ... ]
        >>> reqs = ['incident response']
        >>> body = generate_cover_letter_body(
        ...     achievements=achievements,
        ...     job_requirements=reqs,
        ...     company_name='SecureOps'
        ... )
    """
    # Select proof examples
    proof_examples = select_proof_examples(achievements, job_requirements, top_n=2)
    
    if not proof_examples:
        # Fallback generic body
        return f"I am confident that my experience aligns well with {company_name}'s needs and I would be an excellent addition to your team."
    
    body_paragraphs = []
    
    for requirement, achievement, confidence in proof_examples:
        template = BODY_TEMPLATES.get(style, BODY_TEMPLATES['achievement'])
        
        paragraph = f"My experience with {requirement} directly supports your needs. {achievement}. "
        paragraph += f"I am particularly interested in contributing to {company_name}'s goals in this area."
        body_paragraphs.append(paragraph)
    
    return "\n\n".join(body_paragraphs)


def generate_cover_letter_closing(
    company_name: str,
    primary_skill: str,
    domain: str,
    company_value: str = 'excellence',
    style: str = 'enthusiastic'
) -> str:
    """
    Generate closing paragraph for cover letter.
    
    Args:
        company_name (str): Company name
        primary_skill (str): Primary skill/expertise
        domain (str): Domain
        company_value (str): Company's primary value
        style (str): Style of closing
    
    Returns:
        str: Closing paragraph
    """
    template = CLOSING_TEMPLATES.get(style, CLOSING_TEMPLATES['professional'])
    
    closing = template.format(
        company_name=company_name,
        primary_skill=primary_skill,
        domain=domain,
        company_value=company_value,
        contact_info='[Your Contact Information]'
    )
    
    return closing


def generate_cover_letter(
    name: str,
    job_title: str,
    company_name: str,
    years_experience: int,
    primary_skill: str,
    domain: str,
    achievements: List[Dict[str, Any]],
    job_requirements: List[str],
    job_description: str = '',
    style: str = 'professional'
) -> Dict[str, str]:
    """
    Generate complete cover letter with all sections.
    
    Args:
        name (str): Your name
        job_title (str): Target job title
        company_name (str): Company name
        years_experience (int): Years in field
        primary_skill (str): Primary skill
        domain (str): Domain
        achievements (List[Dict]): Key achievements
        job_requirements (List[str]): Job requirements
        job_description (str): Full job posting (for context)
        style (str): Style/tone
    
    Returns:
        Dict[str, str]: Cover letter with sections and full text
    
    Example:
        >>> cl = generate_cover_letter(
        ...     name='Violet Figueroa',
        ...     job_title='SOC Analyst II',
        ...     company_name='SecureOps',
        ...     years_experience=3,
        ...     primary_skill='SIEM',
        ...     domain='threat detection',
        ...     achievements=[...],
        ...     job_requirements=['SIEM', 'incident response']
        ... )
        >>> print(cl['full_text'])
    """
    company_info = extract_company_info(job_description)
    company_value = company_info.get('values', ['excellence'])[0] if company_info.get('values') else 'excellence'
    
    # Generate sections
    opening = generate_cover_letter_opening(
        job_title, company_name, years_experience, primary_skill, domain,
        style='enthusiastic', company_info=company_info
    )
    body = generate_cover_letter_body(achievements, job_requirements, company_name)
    closing = generate_cover_letter_closing(company_name, primary_skill, domain, company_value)
    
    # Format full cover letter
    today = datetime.now().strftime('%B %d, %Y')
    
    full_text = f"""[Your Address]
[City, State ZIP]

{today}

{company_name}
[Company Address]
[City, State ZIP]

Dear Hiring Manager,

{opening}

{body}

{closing}

Sincerely,

{name}
[Your Email]
[Your Phone]
"""
    
    return {
        'opening': opening,
        'body': body,
        'closing': closing,
        'full_text': full_text,
        'company_info': company_info
    }


def generate_cover_letter_variants(
    name: str,
    job_title: str,
    company_name: str,
    years_experience: int,
    primary_skill: str,
    domain: str,
    achievements: List[Dict[str, Any]],
    job_requirements: List[str],
    job_description: str = ''
) -> Dict[str, Dict[str, str]]:
    """
    Generate multiple cover letter variants (2-3 different styles).
    
    Args:
        (same as generate_cover_letter)
    
    Returns:
        Dict with variants keyed by style
    
    Example:
        >>> variants = generate_cover_letter_variants(...)
        >>> for style, cl in variants.items():
        ...     print(f"\n=== {style.upper()} ===")
        ...     print(cl['full_text'])
    """
    styles = ['enthusiastic', 'professional', 'achievement']
    variants = {}
    
    for style in styles:
        variants[style] = generate_cover_letter(
            name=name,
            job_title=job_title,
            company_name=company_name,
            years_experience=years_experience,
            primary_skill=primary_skill,
            domain=domain,
            achievements=achievements,
            job_requirements=job_requirements,
            job_description=job_description,
            style=style
        )
    
    return variants
