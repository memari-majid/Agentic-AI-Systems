# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by emailing mmemari@uvu.edu.

**Please do not report security vulnerabilities through public GitHub issues.**

## API Key Security

This project uses OpenAI API keys for automated updates. Please follow these security best practices:

### For Repository Maintainers

1. **Never commit API keys**
   - Always use GitHub Secrets for API keys
   - Add `.env` to `.gitignore`
   - Use environment variables for sensitive data

2. **Limit API key permissions**
   - Use separate API keys for different purposes
   - Set spending limits in OpenAI dashboard
   - Regularly rotate API keys

3. **Monitor API usage**
   - Check OpenAI usage dashboard regularly
   - Set up billing alerts
   - Review GitHub Actions logs for anomalies

### For Contributors

1. **If you accidentally commit an API key:**
   - Revoke it immediately in OpenAI dashboard
   - Generate a new key
   - Never reuse exposed keys

2. **Testing locally:**
   - Use `.env` file (not tracked by git)
   - Use `python-dotenv` to load environment variables
   - Never hardcode API keys in code

3. **In pull requests:**
   - Never include API keys in code or comments
   - Use placeholder values in examples
   - Reference environment variables

## GitHub Actions Security

### Workflow Permissions

The automated update workflow requires:
- `contents: write` - To update files
- `issues: write` - To create update reports
- `pull-requests: write` - Optional for PR creation

### Secret Management

Secrets used:
- `OPENAI_API_KEY` - Required for update agent
- `GITHUB_TOKEN` - Automatically provided by GitHub

### Third-party Actions

We use the following trusted GitHub Actions:
- `actions/checkout@v4` - Official GitHub action
- `actions/setup-python@v5` - Official GitHub action
- `actions/upload-artifact@v4` - Official GitHub action
- `actions/github-script@v7` - Official GitHub action

## Dependency Security

### Python Dependencies

All Python dependencies are:
- Pinned to minimum versions in `requirements.txt`
- From trusted sources (PyPI)
- Regularly updated

To check for vulnerabilities:
```bash
pip install pip-audit
pip-audit -r requirements.txt
```

### Updating Dependencies

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## Rate Limiting

The update agent includes rate limiting to prevent:
- API quota exhaustion
- Accidental DDoS on external services
- Excessive costs

Rate limits:
- arXiv searches: 1 second delay between requests
- Link verification: 300ms delay between checks
- OpenAI API: Natural rate limiting via sequential calls

## Cost Controls

To prevent unexpected costs:

1. **OpenAI spending limits**
   - Set in OpenAI dashboard under Billing → Limits
   - Recommended: $10/month for this automation

2. **GitHub Actions limits**
   - Free tier: 2,000 minutes/month
   - This automation uses ~5 minutes/week
   - Estimated: 20 minutes/month

3. **Monitoring**
   - Weekly review of OpenAI usage
   - Monthly review of GitHub Actions usage
   - Set up billing alerts

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Security Updates

We will:
- Address reported vulnerabilities within 7 days
- Update dependencies monthly
- Announce security updates in release notes
- Credit reporters (if desired)

## Best Practices for Users

1. **Fork this repository?**
   - Generate your own OpenAI API key
   - Set up your own GitHub Secrets
   - Review workflow permissions

2. **Cloning locally?**
   - Never share your `.env` file
   - Use virtual environments
   - Keep dependencies updated

3. **Contributing?**
   - Follow security guidelines above
   - Run tests before submitting PR
   - Report security concerns privately

## Compliance

This project:
- Uses OpenAI API in compliance with their usage policies
- Respects arXiv robots.txt and rate limits
- Follows GitHub Actions best practices
- Does not collect or store personal data

## Contact

For security concerns: mmemari@uvu.edu  
For general questions: Open a GitHub issue

---

**Last Updated**: 2025-11-15  
**Version**: 1.0.0

