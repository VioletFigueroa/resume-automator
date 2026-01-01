# Contributing to Resume Automator

Thank you for interest in contributing! This guide explains how to contribute.

## Code of Conduct

Be respectful, inclusive, and professional.

## Getting Started

### Prerequisites

- Python 3.8+
- pip or poetry
- Git

### Local Setup

```bash
git clone https://github.com/VioletFigueroa/resume-automator.git
cd resume-automator
pip install -r requirements.txt
python3 src/generate.py
```

## Making Changes

### Code Style

- Follow PEP 8 Python standards
- Use meaningful variable names
- Add docstrings for functions
- Include comments for complex logic

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type: short description

Longer explanation if needed
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat: add PDF generation`
- `fix: handle special characters in names`
- `docs: update setup instructions`

### Testing

- Test with sample data
- Verify generated resumes
- Check output formatting
- Validate JSON parsing

## Submitting Changes

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly
5. Commit with descriptive messages
6. Push to your fork
7. Open a Pull Request with:
   - Clear title
   - Description of changes
   - Why the change is needed
   - Link to related issues if any

### PR Checklist

- [x] Code follows PEP 8
- [x] Changes are tested
- [x] Documentation updated (if needed)
- [x] Commit messages are clear
- [x] No breaking changes

## Areas for Contribution

### Code

- [ ] Additional output formats
- [ ] New template types
- [ ] Better configuration options
- [ ] Performance improvements
- [ ] Error handling

### Documentation

- [ ] Clarify existing docs
- [ ] Add more examples
- [ ] Fix typos
- [ ] Improve setup instructions

### Community

- [ ] Help answer issues
- [ ] Share resume templates
- [ ] Provide feedback
- [ ] Report bugs

## Security & Privacy

When contributing:
- Never commit real PII or sensitive data
- Keep public data as examples/placeholders
- Document security considerations
- Test with both public and private data

## Reporting Issues

Include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and OS
- Error messages

## Questions?

- Check [docs/](./docs/) for documentation
- Read [../README.md](../README.md) for overview
- Open an issue for help

## License

By contributing, you agree your contributions are licensed under MIT License.

## Recognition

Contributors will be:
- Added to acknowledgments in README
- Mentioned in release notes
- Credited in git history

Thank you! 🎉
