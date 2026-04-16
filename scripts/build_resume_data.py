from __future__ import annotations

import re
import textwrap
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "Data"
OUTPUT_DIR = DATA_DIR / "generated"
AVATAR_CACHE_DIR = ROOT / ".output"


def load_yaml(name: str) -> dict[str, Any]:
    with (DATA_DIR / name).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def latex_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def clean_markup(text: str) -> str:
    stripped = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", stripped).strip()


def collapse_sentence(text: str, max_len: int = 180) -> str:
    normalized = clean_markup(text)
    if len(normalized) <= max_len:
        return normalized
    def cleanup(fragment: str) -> str:
        fragment = fragment.rstrip(",;:- ")
        if fragment.count("(") > fragment.count(")"):
            fragment = fragment.rsplit("(", 1)[0].rstrip(",;:- ")
        return fragment
    punctuation_positions = [normalized.rfind(mark, 0, max_len) for mark in [". ", "; ", ": "]]
    punctuation_cut = max(punctuation_positions)
    if punctuation_cut > int(max_len * 0.55):
        return cleanup(normalized[: punctuation_cut + 1].strip())
    trimmed = cleanup(normalized[: max_len - 3].rsplit(" ", 1)[0])
    return f"{trimmed}..."


def format_date_label(raw: str | date | datetime | None) -> str:
    if not raw:
        return ""
    if isinstance(raw, datetime):
        parsed = raw.date()
    elif isinstance(raw, date):
        parsed = raw
    else:
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            return str(raw)
    if parsed.year == date.today().year:
        return parsed.strftime("%b. %Y")
    return parsed.strftime("%Y")


def sort_by_start_date(items: list[dict[str, Any]], field: str) -> list[dict[str, Any]]:
    def key(item: dict[str, Any]) -> str:
        value = item.get(field, "")
        if isinstance(value, datetime):
            return value.date().isoformat()
        if isinstance(value, date):
            return value.isoformat()
        return str(value)

    return sorted(items, key=key, reverse=True)


def wrap_command(command: str) -> str:
    lines = textwrap.wrap(command, width=96, break_long_words=False, break_on_hyphens=False)
    return "\n".join(lines) if lines else command


def href(url: str, label: str) -> str:
    if not url:
        return latex_escape(label)
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url) or url.startswith("mailto:") or url.startswith("tel:"):
        target = url
    else:
        normalized = url.replace("\\", "/")
        target = "run:" + urllib.parse.quote(normalized, safe="/:._-()")
    return rf"\resumeLinkText{{{target}}}{{{latex_escape(label)}}}"


def join_links(links: list[str]) -> str:
    return r" \textcolor{ResumeTextMuted}{|} ".join(link for link in links if link)


def maybe_download_avatar(avatar_ref: str | None) -> tuple[str | None, str]:
    initials = "ZE"
    if not avatar_ref:
        return None, initials
    parsed = urllib.parse.urlparse(avatar_ref)
    if parsed.scheme in {"http", "https"}:
        extension = Path(parsed.path).suffix or ".jpg"
        AVATAR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        target = AVATAR_CACHE_DIR / f"resume-avatar{extension}"
        try:
            urllib.request.urlretrieve(avatar_ref, target)
            return target.relative_to(ROOT).as_posix(), initials
        except Exception:
            return target.relative_to(ROOT).as_posix(), initials
    local_path = (ROOT / avatar_ref).resolve() if not Path(avatar_ref).is_absolute() else Path(avatar_ref)
    if local_path.exists():
        try:
            return local_path.relative_to(ROOT).as_posix(), initials
        except ValueError:
            return local_path.as_posix(), initials
    return None, initials


def render_header(config: dict[str, Any], profile: dict[str, Any]) -> str:
    avatar_path, initials = maybe_download_avatar(config.get("avatar"))
    avatar = (
        rf"\resumeAvatarAuto{{{avatar_path}}}{{{initials}}}"
        if avatar_path
        else rf"\resumeAvatarPlaceholder{{{initials}}}"
    )

    name = latex_escape(config.get("name", ""))
    title = latex_escape(config.get("title") or config.get("position") or "")
    tagline = latex_escape(config.get("tagline") or profile.get("about", {}).get("summary", ""))

    contact_bits = [
        latex_escape(config.get("affiliation", "")),
        latex_escape(config.get("location", "")),
        href(f"mailto:{config.get('email', '')}", config.get("email", "")) if config.get("email") else "",
        href(f"tel:{config.get('phone', '').replace(' ', '')}", config.get("phone", "")) if config.get("phone") else "",
    ]
    links_data = config.get("contact_links") or []
    if not links_data:
        fallback_map = {
            "Homepage": config.get("homepage_link"),
            "GitHub": config.get("github_link"),
            "Google Scholar": config.get("google_scholar"),
            "CV": config.get("cv_link"),
        }
        links_data = [{"label": label, "url": url} for label, url in fallback_map.items() if url]

    header_links = [href(item.get("url", ""), item.get("label", "")) for item in links_data]
    contact_line = join_links([bit for bit in contact_bits if bit])
    links_line = join_links(header_links)
    return wrap_command(rf"\resumeHeader{{{avatar}}}{{{name}}}{{{title}}}{{{tagline}}}{{{contact_line}}}{{{links_line}}}")


def render_about(profile: dict[str, Any]) -> str:
    about = profile.get("about") or {}
    focus = about.get("focus_areas") or []
    lead = collapse_sentence(about.get("lead", ""), 150)
    focus_sentence = ""
    if focus:
        focus_sentence = "Focused on " + ", ".join(clean_markup(item) for item in focus[:4]) + "."
    else:
        focus_sentence = collapse_sentence(about.get("summary", ""), 150)
    sentence = " ".join(part for part in [lead, focus_sentence] if part).strip()
    content = [rf"\resumeSummary{{{latex_escape(sentence)}}}"]
    if focus:
        tags = " ".join(rf"\resumeTag{{{latex_escape(item)}}}" for item in focus[:5])
        content.append(tags)
    return "\n".join(content)


def render_education(entries: list[dict[str, Any]]) -> str:
    blocks: list[str] = []
    for item in sort_by_start_date(entries, "start_date"):
        school = href(item.get("link", ""), item.get("school", ""))
        program = latex_escape(item.get("program", ""))
        period = latex_escape(item.get("period", ""))
        focus = latex_escape(collapse_sentence(item.get("focus", ""), 130))
        blocks.append(rf"\resumeEntry{{{school}}}{{{program}}}{{{period}}}{{{focus}}}")
        highlights = item.get("highlights") or []
        if highlights:
            blocks.append(r"\resumeBulletsStart")
            for bullet in highlights[:3]:
                blocks.append(rf"\resumeBullet{{{latex_escape(clean_markup(bullet))}}}")
            blocks.append(r"\resumeBulletsEnd")
        blocks.append(r"\vspace{0.45em}")
    return "\n".join(blocks[:-1] if blocks else blocks)


def project_bullets(item: dict[str, Any]) -> list[str]:
    bullets: list[str] = []
    description = item.get("description")
    if description:
        bullets.append(collapse_sentence(description, 170))
    tech = clean_markup(item.get("tech_stack", ""))
    outcome = clean_markup(item.get("outcome", ""))
    tail_parts = []
    if tech:
        tail_parts.append(f"Tech: {tech}.")
    if outcome:
        tail_parts.append(outcome if outcome.endswith(".") else f"{outcome}.")
    if tail_parts:
        bullets.append(" ".join(tail_parts))
    return bullets[:2]


def project_display_title(title: str) -> str:
    normalized = clean_markup(title)
    if " with " in normalized:
        normalized = normalized.split(" with ", 1)[0]
    if " and " in normalized and len(normalized) > 52:
        normalized = normalized.split(" and ", 1)[0]
    return normalized


def render_projects(entries: list[dict[str, Any]], limit: int) -> str:
    blocks: list[str] = []
    for item in sort_by_start_date(entries, "date")[:limit]:
        title = href(item.get("link", ""), project_display_title(item.get("title", "")))
        subtitle_parts = [item.get("attribute", ""), item.get("tech_stack", "")]
        subtitle = " | ".join(part for part in subtitle_parts if part)
        period = format_date_label(item.get("date"))
        blocks.append(rf"\resumeEntry{{{title}}}{{{latex_escape(subtitle)}}}{{{latex_escape(period)}}}{{}}")
        blocks.append(r"\resumeBulletsStart")
        for bullet in project_bullets(item):
            blocks.append(rf"\resumeBullet{{{latex_escape(bullet)}}}")
        blocks.append(r"\resumeBulletsEnd")
        blocks.append(r"\vspace{0.38em}")
    return "\n".join(blocks[:-1] if blocks else blocks)


def render_awards(entries: list[dict[str, Any]], limit: int) -> str:
    lines = [r"\resumeCompactListStart"]
    for item in sort_by_start_date(entries, "date")[:limit]:
        award = latex_escape(item.get("award_description", ""))
        contest = latex_escape(item.get("title", ""))
        detail = collapse_sentence(item.get("reason", ""), 110)
        year = format_date_label(item.get("date"))
        sentence = rf"\textbf{{{award}}}, {contest} \hfill \textcolor{{ResumeTextMuted}}{{{latex_escape(year)}}}"
        if detail:
            sentence += rf"\\[-0.15em]\textcolor{{ResumeTextMuted}}{{{latex_escape(detail)}}}"
        lines.append(rf"\resumeCompactItem{{{sentence}}}")
    lines.append(r"\resumeCompactListEnd")
    return "\n".join(lines)


def render_publications(entries: list[dict[str, Any]], limit: int) -> str:
    lines = [r"\resumeCompactListStart"]
    for item in entries[:limit]:
        title = href(item.get("pdf", "") or item.get("page", ""), clean_markup(item.get("title", "")))
        conference = latex_escape(clean_markup(item.get("conference", "")))
        notes = latex_escape(clean_markup(item.get("notes", "")))
        bits = [rf"\textbf{{{title}}}", conference]
        if notes:
            bits.append(rf"\textcolor{{ResumeTextMuted}}{{{notes}}}")
        lines.append(rf"\resumeCompactItem{{{' '.join(bit for bit in bits if bit)}}}")
    lines.append(r"\resumeCompactListEnd")
    return "\n".join(lines)


def render_skills(profile: dict[str, Any]) -> str:
    skill_groups = profile.get("skills") or []
    lines = [r"\resumeCompactListStart"]
    for group in skill_groups:
        title = latex_escape(group.get("title", ""))
        items = ", ".join(clean_markup(item) for item in (group.get("items") or []))
        lines.append(rf"\resumeCompactItem{{\textbf{{{title}}}: {latex_escape(items)}}}")
    lines.append(r"\resumeCompactListEnd")
    return "\n".join(lines)


def render_section(title: str, body: str) -> str:
    return wrap_command(rf"\resumeSectionBlock{{\section{{{latex_escape(title)}}}}}{{{body}}}")


def build_body() -> str:
    config = load_yaml("_config.yml")
    profile = load_yaml("profile.yml")
    education = load_yaml("education.yml").get("main") or []
    projects = load_yaml("project.yml").get("main") or []
    awards = load_yaml("awards.yml").get("main") or []
    publications = load_yaml("publications.yml").get("main") or []

    visibility = config.get("section_visibility") or {}
    preview = config.get("list_preview_count") or {}
    theme = config.get("theme") or {}

    parts = [
        rf"\resumeSetAccent{{{theme.get('accent_color', '1F4E79')}}}{{{theme.get('accent_soft_color', 'EAF2F8')}}}",
        render_header(config, profile),
    ]

    if visibility.get("about", True):
        parts.append(render_section("Profile", render_about(profile)))
    if visibility.get("education", True) and education:
        parts.append(render_section("Education", render_education(education)))
    if visibility.get("projects", True) and projects:
        parts.append(render_section("Selected Projects", render_projects(projects, int(preview.get("projects", 5)))))
    if visibility.get("awards", True) and awards:
        parts.append(render_section("Awards", render_awards(awards, int(preview.get("awards", 4)))))
    if visibility.get("publications", False) and publications:
        parts.append(
            render_section("Publications", render_publications(publications, int(preview.get("publications", 3))))
        )
    if visibility.get("skills", True):
        parts.append(render_section("Skills", render_skills(profile)))

    return "\n\n".join(parts) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / "resume-body.tex"
    output.write_text(build_body(), encoding="utf-8")


if __name__ == "__main__":
    main()
