"""LEGION Website QA NCA — deterministic static checks on owned synthetic HTML.

This is NOT a browser, a WCAG conformance test or OWASP penetration test.
No HTTP, shell, client website access, automation or commercial permissions.
Six narrowly scoped heuristics, each backed by an independently labeled exam.
"""
from __future__ import annotations

import hashlib
import re
from html.parser import HTMLParser

MAX_HTML_CHARS = 40_000
MAX_ISSUES = 512
CHECKS = frozenset({
    "MISSING_HTML_LANG", "EMPTY_PAGE_TITLE", "IMAGE_MISSING_ALT",
    "LINK_MISSING_NAME", "INPUT_MISSING_LABEL", "HEADING_LEVEL_SKIP",
})


class LocalReviewDenied(ValueError):
    """Fail-closed local input and document constraints."""


class _Structure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title_text = []
        self.title_depth = 0
        self.headings = []
        self.issues = []
        self.links = []
        self.link_stack = []
        self.labels = set()
        self.label_depth = 0
        self.inputs = []
        self._seen_html = False
        self._seen_title = False
        self._seen_main = False

    def _finding(self, code: str, line: int) -> None:
        if len(self.issues) >= MAX_ISSUES:
            raise LocalReviewDenied("TOO_MANY_ISSUES")
        self.issues.append({"code":code, "line":line})

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        line = self.getpos()[0]
        if tag == "html" and not self._seen_html:
            self._seen_html = True
            self.lang = (data.get("lang") or "").strip()
        if tag == "title":
            self._seen_title = True
            self.title_depth += 1
        if tag == "main":
            self._seen_main = True
        if tag == "img":
            if "alt" not in data:
                self._finding("IMAGE_MISSING_ALT", line)
            if self.link_stack and (data.get("alt") or "").strip():
                self.link_stack[-1]["names"].append(data["alt"])
        if tag == "a" and "href" in data:
            self.link_stack.append({
                "line":line,
                "names":[],
                "aria":bool((data.get("aria-label") or "").strip()
                            or (data.get("aria-labelledby") or "").strip()),
            })
        if tag == "label":
            self.label_depth += 1
            if (data.get("for") or "").strip():
                self.labels.add(data["for"].strip())
        if tag == "input" and data.get("type", "").lower() != "hidden":
            self.inputs.append({
                "line":line, "id":(data.get("id") or "").strip(),
                "name":bool((data.get("aria-label") or "").strip()
                             or (data.get("aria-labelledby") or "").strip()),
                "wrapped":self.label_depth > 0,
            })
        match = re.fullmatch(r"h([1-6])", tag)
        if match:
            self.headings.append((int(match.group(1)), line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in ("a", "label", "title"):
            self.handle_endtag(tag)

    def handle_data(self, data):
        if self.title_depth:
            self.title_text.append(data)
        if self.link_stack:
            for link in self.link_stack:
                link["names"].append(data)

    def handle_endtag(self, tag):
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        if tag == "label" and self.label_depth:
            self.label_depth -= 1
        if tag == "a" and self.link_stack:
            link = self.link_stack.pop()
            if not (link["aria"] or "".join(link["names"]).strip()):
                self._finding("LINK_MISSING_NAME", link["line"])

    def finish(self):
        if not self.lang:
            self._finding("MISSING_HTML_LANG", 1)
        if not "".join(self.title_text).strip():
            self._finding("EMPTY_PAGE_TITLE", 1)
        for inp in self.inputs:
            if not (inp["name"] or inp["wrapped"] or
                    (inp["id"] and inp["id"] in self.labels)):
                self._finding("INPUT_MISSING_LABEL", inp["line"])
        previous = 0
        for level, line in self.headings:
            if previous and level > previous + 1:
                self._finding("HEADING_LEVEL_SKIP", line)
            previous = level
        # Unclosed links are treated as incomplete source, not silently
        # accepted as safe. The synthetic fixture corpus is well-formed.
        if self.link_stack:
            raise LocalReviewDenied("UNCLOSED_LINK")
        return tuple(sorted(self.issues, key=lambda x: (x["line"], x["code"])))


def scan_html(html: str) -> dict:
    """Return *only* reproducible static findings for a local text snapshot."""
    if type(html) is not str or not 0 < len(html) <= MAX_HTML_CHARS or "\x00" in html:
        raise LocalReviewDenied("INVALID_HTML_INPUT")
    detector = _Structure()
    try:
        detector.feed(html)
        detector.close()
        issues = detector.finish()
    except (AssertionError, RecursionError, OverflowError) as exc:
        raise LocalReviewDenied("INVALID_HTML_STRUCTURE") from None
    if not detector._seen_html:
        raise LocalReviewDenied("MISSING_HTML_ROOT")
    return {
        "document_sha256":hashlib.sha256(html.encode("utf-8")).hexdigest(),
        "checks":len(CHECKS),
        "findings":list(issues),
        "finding_codes":sorted({x["code"] for x in issues}),
        "total_findings":len(issues),
        "review_scope":"STATIC_HTML_HEURISTICS_ONLY",
        "wcag_conformant":False,
        "owasp_security_verified":False,
        "browser_executed":False,
        "client_site_access":False,
        "commercial_platform_access":False,
        "professional_qualified":False,
        "production_authorized":False,
    }
