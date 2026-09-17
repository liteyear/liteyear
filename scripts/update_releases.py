"""Refresh verified public release metadata; retain the good snapshot on failure."""
import datetime as dt
import json
import os
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = (("ableton-now-playing", "Ableton Now Playing"), ("NEXP.FM-2.0", "NEXP.FM"))


def fetch_release(repo):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "liteyear-profile", "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    request = urllib.request.Request(f"https://api.github.com/repos/liteyear/{repo}/releases/latest", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def date_label(value):
    return value.strftime("%B ") + str(value.day) + value.strftime(", %Y")


def render(releases, today):
    rows = ["| Project | Latest release | Published |", "| :--- | :--- | :--- |"]
    for (repo, label), release in zip(PROJECTS, releases, strict=True):
        url, tag = release["html_url"], release["tag_name"]
        if release.get("draft") or release.get("prerelease"):
            raise ValueError("Expected a published stable release")
        if not url.startswith(f"https://github.com/liteyear/{repo}/releases/tag/"):
            raise ValueError("Unexpected release URL")
        if not re.fullmatch(r"[A-Za-z0-9._+-]{1,64}", tag):
            raise ValueError("Unexpected release tag")
        if any(char in url for char in "\n\r|()<> "):
            raise ValueError("Unsafe release URL")
        published = dt.datetime.fromisoformat(release["published_at"].replace("Z", "+00:00"))
        rows.append(f"| {label} | [{tag}]({url}) | {date_label(published)} |")
    rows += ["", f"<sub>Public release data checked {date_label(today)} (UTC). Refreshed daily; the last successful snapshot stays visible if a refresh is unavailable.</sub>"]
    return "\n".join(rows)


def main():
    releases = [fetch_release(repo) for repo, _ in PROJECTS]
    content = render(releases, dt.datetime.now(dt.timezone.utc))
    path = ROOT / "README.md"
    original = path.read_text()
    start, end = "<!-- RELEASES:START -->", "<!-- RELEASES:END -->"
    if original.count(start) != 1 or original.count(end) != 1:
        raise ValueError("Release markers must exist exactly once")
    before, rest = original.split(start)
    _, after = rest.split(end)
    updated = before + start + "\n" + content + "\n" + end + after
    if updated != original:
        temporary = path.with_suffix(".tmp")
        temporary.write_text(updated)
        temporary.replace(path)


if __name__ == "__main__":
    main()
