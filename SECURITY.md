# Security Notice

## API Key Management

**⚠️ IMPORTANT:** Never commit API keys to version control.

### If you accidentally exposed an API key:

1. **Regenerate immediately** at https://platform.openai.com/api-keys
2. Update your local `.env` file with the new key
3. Rotate any other credentials that may have been exposed

### Safe practices:

- ✅ Use `.env` for local development (already in `.gitignore`)
- ✅ Use environment variables in production
- ✅ Use `.env.example` with placeholder values only
- ❌ Never commit `.env` to git
- ❌ Never hardcode API keys in source code
- ❌ Never share API keys in documentation or examples

### Files already protected:

- `.env` is in `.gitignore`
- `.env.example` contains only placeholder values

### Version history:

The initial commit contained a malformed placeholder key in `.env.example` that has since been replaced with a proper placeholder. If you're forking this repository, make sure to:

1. Copy `.env.example` to `.env`
2. Replace the placeholder with your actual API key
3. Never commit `.env` to your fork
