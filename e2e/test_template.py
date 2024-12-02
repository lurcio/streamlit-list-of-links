from pathlib import Path

import pytest

from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
BASIC_EXAMPLE_FILE = ROOT_DIRECTORY / "list_of_links" / "example.py"

@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(BASIC_EXAMPLE_FILE) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for app to load
    page.get_by_role("img", name="Running...").is_hidden()


def test_should_render_template(page: Page):
    frame_0 = page.frame_locator(
        'iframe[title="list_of_links\\.list_of_links"]'
    ).nth(0)
    frame_1 = page.frame_locator(
        'iframe[title="list_of_links\\.list_of_links"]'
    ).nth(1)

    st_markdown_0 = page.get_by_role('paragraph').nth(0)
    st_markdown_1 = page.get_by_role('paragraph').nth(1)

    expect(st_markdown_0).to_contain_text("You chose link target 0!")

    frame_0.get_by_role("link", name="Bob").click()

    expect(st_markdown_0).to_contain_text("You chose link target 1!")
    expect(st_markdown_1).to_contain_text("You chose link target 0!")

    frame_1.get_by_role("link", name="Bob").click()
    frame_1.get_by_role("link", name="David").click()

    expect(st_markdown_0).to_contain_text("You chose link target 1!")
    expect(st_markdown_1).to_contain_text("You chose link target 3!")

    page.get_by_label("Enter a title").click()
    page.get_by_label("Enter a title").fill("Test Title")
    page.get_by_label("Enter a title").press("Enter")

    expect(frame_1.get_by_text("Test Title")).to_be_visible()

    frame_1.get_by_role("link", name="Alice").click()

    expect(st_markdown_0).to_contain_text("You chose link target 1!")
    expect(st_markdown_1).to_contain_text("You chose link target 0!")


def test_should_change_iframe_height(page: Page):
    frame = page.frame_locator('iframe[title="list_of_links\\.list_of_links"]').nth(1)

    expect(frame.get_by_text("Streamlit")).to_be_visible()

    locator = page.locator('iframe[title="list_of_links\\.list_of_links"]').nth(1)

    page.wait_for_timeout(1000)
    init_frame_height = locator.bounding_box()['height']
    assert init_frame_height != 0

    page.get_by_label("Enter a title").click()

    page.get_by_label("Enter a title").fill(35 * "Streamlit ")
    page.get_by_label("Enter a title").press("Enter")

    expect(frame.get_by_text("Streamlit Streamlit Streamlit")).to_be_visible()

    page.wait_for_timeout(1000)
    frame_height = locator.bounding_box()['height']
    assert frame_height > init_frame_height

    page.set_viewport_size({"width": 150, "height": 150})

    expect(frame.get_by_text("Streamlit Streamlit Streamlit")).not_to_be_in_viewport()

    page.wait_for_timeout(1000)
    frame_height_after_viewport_change = locator.bounding_box()['height']
    assert frame_height_after_viewport_change > frame_height
