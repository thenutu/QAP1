import re
import time
from pathlib import Path
from playwright.sync_api import expect

BASE = "https://practice.expandtesting.com"

def test_practice_site_login(page, tmp_path):
    """
    Demo flow against ExpandTesting Practice site.
    - Navigate to the Login page
    - Attempt a login (intentionally bad creds to trigger an error state)
    - Capture screenshot + trace for visual review
    """
    # Start Playwright tracing for post-run playback in Trace Viewer
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # Go to the Login page
    page.goto(f"{BASE}/login")

    # Fill the form — selectors are generic and may need tweaking if the site updates
    page.locator('input[name="username"]').fill("practice_user")
    page.locator('input[name="password"]').fill("wrong_password")
    page.locator('button[type="submit"]').click()

    # Expect to remain on the login page (invalid creds) or be redirected if demo creds exist
    expect(page).to_have_url(re.compile(r"/login|/profile|/dashboard"))

    # Save artifacts for review
    ts = int(time.time())
    screenshot_path = tmp_path / f"screenshot_{ts}.png"
    trace_path = tmp_path / f"trace_{ts}.zip"

    page.screenshot(path=str(screenshot_path), full_page=True)
    page.context.tracing.stop(path=str(trace_path))

    print(f"Saved screenshot: {screenshot_path}")
    print(f"Saved trace: {trace_path}")
