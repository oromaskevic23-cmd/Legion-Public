"""Real Chromium behavioral probes on *owned synthetic* HTML only.

Not a general-purpose web browsing tool or WCAG certificate. No customer URLs,
credentials, persistent storage, browser downloads, or external side effects.
Browser emulated offline + request routing are defense in depth, not an OS sandbox.
"""
from __future__ import annotations

import hashlib

MAX_HTML_CHARS = 10_000
CATEGORIES = frozenset({"click", "keyboard", "label", "status", "disclosure", "form"})


class BrowserQADenied(ValueError):
    """Reject unsafe inputs and capability requests."""


def probe(browser, html: str, category: str) -> dict:
    """Observe the behavior of a local synthetic document; never read oracle labels."""
    if (type(html) is not str or not 0 < len(html) <= MAX_HTML_CHARS
            or "\x00" in html or type(category) is not str
            or category not in CATEGORIES):
        raise BrowserQADenied("INVALID_SYNTHETIC_BROWSER_INPUT")
    # This is an additional conservative filter, NOT an HTML sanitizer. Run only
    # the repository-owned frozen fixtures, not user-submitted or third-party HTML.
    lowered = html.lower()
    if any(word in lowered for word in (
        "http:", "https:", "file:", "src=", "<iframe", "<object",
        "websocket", "webrtc", "worker", "import(", "fetch(", "xmlhttprequest",
        "window.open", "location.", "<base", "<meta http-equiv",
    )):
        raise BrowserQADenied("EXTERNAL_CAPABILITY_NOT_PERMITTED")
    context = browser.new_context(
        offline=True, service_workers="block", accept_downloads=False,
        permissions=[], java_script_enabled=True,
    )
    attempts = []
    context.on("request", lambda request: attempts.append(request.url))
    context.route("**/*", lambda route: route.abort())
    try:
        page = context.new_page()
        page.set_default_timeout(2500)
        page.set_content(html, wait_until="load", timeout=5000)
        passed = False
        if category == "click":
            page.get_by_role("button", name="Increase").click()
            passed = page.locator("#count").inner_text() == "1"
        elif category == "keyboard":
            page.keyboard.press("Tab")
            passed = page.evaluate("document.activeElement?.id === 'target'")
        elif category == "label":
            passed = page.get_by_role("textbox", name="Email").count() == 1
        elif category == "status":
            page.get_by_role("button", name="Save").click()
            passed = (page.get_by_role("status").count() == 1 and
                      page.get_by_role("status").inner_text() == "Saved")
        elif category == "disclosure":
            page.get_by_role("button", name="Details").click()
            passed = (page.get_by_role("button", name="Details").get_attribute("aria-expanded") == "true"
                      and page.locator("#panel").is_visible())
        elif category == "form":
            page.get_by_role("button", name="Submit").click()
            passed = (page.locator("#email").evaluate("el => !el.validity.valid")
                      and page.locator("#sent").inner_text() == "no")
        if attempts:
            raise BrowserQADenied("EXTERNAL_NETWORK_ATTEMPTED")
        return {
            "observed_pass": bool(passed),
            "category": category,
            "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
            "browser_executed": True,
            "network_attempts": 0,
            "commercial_platform_access": False,
            "production_authorized": False,
        }
    finally:
        context.close()
