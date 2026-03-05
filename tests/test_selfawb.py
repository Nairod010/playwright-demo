import re
import pathlib
from playwright.sync_api import Playwright, expect


def test_self_awb_standard(playwright: Playwright) -> None:
    video_dir = pathlib.Path("test-artifacts/videos")
    video_dir.mkdir(parents=True, exist_ok=True)

    # browser = playwright.chromium.launch(headless=True)

    browser = playwright.firefox.launch(headless=True)

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

    page.locator("input[name=\"recipientName\"]").click()
    page.locator("input[name=\"recipientName\"]").fill("test")
    page.locator("input[name=\"recipientPhone1\"]").click()
    page.locator("input[name=\"recipientPhone1\"]").fill("721622436")

    page.get_by_role("combobox", name="Judet").click()
    page.get_by_role("combobox", name="Judet").fill("bucure")
    page.get_by_role("option", name="Bucuresti").click()
    page.get_by_role("combobox").nth(4).click()
    page.get_by_role("combobox").nth(4).fill("1 mai")
    page.get_by_role("option", name="Mai (Bulevard)").click()
    page.locator("input[name=\"recipientNo\"]").click()
    page.locator("input[name=\"recipientNo\"]").fill("1")
    page.locator("input[name=\"height\"]").click()
    page.locator("input[name=\"height\"]").fill("12")
    page.locator("input[name=\"width\"]").click()
    page.locator("input[name=\"width\"]").fill("12")
    page.locator("input[name=\"length\"]").click()
    page.locator("input[name=\"length\"]").fill("12")
    

    page.wait_for_timeout(1500)
    page.get_by_role("button", name="Salveaza", exact=True).click()
    page.wait_for_timeout(1500)

    awb_box = page.locator(".css-4l6sa6")
    expect(awb_box).to_be_visible()

    awb = awb_box.inner_text().strip()
    print(f"Generated value: {awb}")

    expect(awb_box).to_have_text(re.compile(r"^7\d{12}$"))
    assert re.fullmatch(r"7\d{12}", awb), f"AWB did not match expected format: {awb}"

    page.get_by_role("button", name="Print").click()

    context.close()
    browser.close()

    print(f"Video(s) saved under: {video_dir.resolve()}")