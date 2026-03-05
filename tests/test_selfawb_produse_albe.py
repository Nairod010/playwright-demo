import re
import pathlib
from playwright.sync_api import Playwright, expect


def test_self_awb_incompatibilitate_optiuni(playwright: Playwright) -> None:
    video_dir = pathlib.Path("test-artifacts/videos")
    video_dir.mkdir(parents=True, exist_ok=True)

    browser = playwright.chromium.launch(headless=True)

    context = browser.new_context(
        record_video_dir=str(video_dir),
        record_video_size={"width": 1280, "height": 720}, 
    )

    page = context.new_page()
    page.goto("https://www.selfawb.ro/new/login")

    page.locator("input[name=\"username\"]").click()
    page.locator("input[name=\"username\"]").fill("clienttest")
    page.locator("input[name=\"password\"]").click()
    page.locator("input[name=\"password\"]").fill("testing")
    page.get_by_role("button", name="Autentificare").click()

    page.get_by_role("textbox", name="Cauta contul...").click()
    page.get_by_role("textbox", name="Cauta contul...").fill("test")
    page.get_by_role("button", name="FAN Courier - cont test").click()

    page.get_by_role("button", name="AWB").click()
    page.get_by_role("link", name="Expediere interna", exact=True).click()

    page.get_by_role("button", name="Adauga din lista de").click()
    page.get_by_role("button", name="Adauga destinatar nou Introdu").click()
    page.get_by_role("button", name="Adauga din lista de").click()
    page.get_by_role("checkbox").nth(2).check()
    
    page.get_by_role("button", name="Deschidere la livrare Ofera").click()
    page.get_by_role("button", name="oPOD Transmite expeditorului").click()

    page.locator("input[name=\"height\"]").click()
    page.locator("input[name=\"height\"]").fill("12")
    page.locator("input[name=\"width\"]").click()
    page.locator("input[name=\"width\"]").fill("12")
    page.locator("input[name=\"length\"]").click()
    page.locator("input[name=\"length\"]").fill("12")

    page.get_by_role("button", name="Salveaza", exact=True).click()

    warning_message = page.locator(".css-166orlq")
    expect(warning_message).to_be_visible()

    incompatible_options = warning_message.inner_text().strip()
    print(f"Warning message:{incompatible_options}")
    expected_message = "Optiunile alese sunt valabile doar cand plata expedierii este la expeditor"
    expect(warning_message).to_have_text(re.compile(expected_message))
    assert re.fullmatch(expected_message, incompatible_options), f"Message not show, got this {incompatible_options}"

    context.close()
    browser.close()

