# Resume

This resume is now data-driven.

1. Update the content in `Data/*.yml`.
2. Run `python scripts/build_resume_data.py` to regenerate `Data/generated/resume-body.tex`.
3. Compile `main.tex` with XeLaTeX.

The generator automatically:

- selects concise resume-ready content from the richer homepage data
- enables clickable links for contact info, schools, projects, and publications
- tries to cache the avatar from `Data/_config.yml`, with a placeholder fallback if download is unavailable
- respects section visibility and preview counts from `Data/_config.yml`
