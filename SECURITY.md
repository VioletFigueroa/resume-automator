# Security Policy

## Scope

This is a portfolio project demonstrating Python automation, system architecture, and secure development practices for personal productivity tools.

## Supported Versions

This project is actively maintained as a personal tool and portfolio demonstration.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

I appreciate security feedback and use it to improve the tool:

- **Email:** violet@violetfigueroa.com
- **Response Time:** Best effort (typically 2-7 days)
- **Recognition:** Security findings will be acknowledged in this SECURITY.md file

## Security Features Implemented

This project demonstrates understanding of the following security concepts:

### PII Protection & Data Security
- **Private data isolation** - Separation of public/private directories
- **Git ignore strategy** - Sensitive data never committed to version control
- **Template-based approach** - Public examples contain no real PII
- **Secure workflow design** - Tool uses private data locally only

### Input Validation & Sanitization
- **JSON schema validation** for profile data structure
- **Path validation** prevents directory traversal
- **File type validation** for generated outputs
- **Safe string handling** in Jinja2 templates

### Secure Development Practices
- **Dependency management** with requirements.txt
- **Environment isolation** through virtual environments
- **Error handling** without exposing sensitive paths
- **Code organization** separates security-critical from general code

### File System Security
- **Secure temp file handling** for PDF generation
- **Permission verification** before file operations
- **Path sanitization** prevents unauthorized file access
- **Output directory isolation** from source code

## Security Considerations for Users

When using this tool:

1. **Never commit private/** directory to version control
2. **Store credentials separately** (not in profile JSON)
3. **Review generated output** before sharing publicly
4. **Keep dependencies updated** for security patches
5. **Use virtual environments** to isolate dependencies

## Known Limitations

As a personal automation tool:

- **No authentication/authorization** - Designed for local single-user use
- **No encryption at rest** - Relies on filesystem permissions
- **No audit logging** - Not designed for multi-user or enterprise use
- **No rate limiting** - Assumes trusted local usage
- **Basic input validation** - Trusts profile JSON structure

This tool is **not designed for**:
- Multi-user environments
- Web deployment
- Processing untrusted data
- Enterprise compliance requirements

## Security Mindset

This project demonstrates security principles even in a personal tool:

1. **Secure by design** - PII separation from day one
2. **Defense in depth** - Multiple layers of data protection
3. **Principle of least privilege** - Tool accesses only necessary files
4. **Fail securely** - Errors don't expose sensitive information
5. **Privacy-first** - No telemetry, no external data transmission

## Dependencies Security

Key dependencies and their security considerations:

- **Jinja2** - Template engine (XSS-safe by default)
- **WeasyPrint** - PDF generation (sandboxed rendering)
- **Python 3.8+** - Modern Python with security patches

Run `pip list --outdated` regularly to check for updates.

## Security Acknowledgments

None at this time. Be the first to provide constructive security feedback!

---

**Last Updated:** January 30, 2026  
**Project Status:** Active Personal Tool / Portfolio Demonstration
