import pathlib
import pytest

def pytest_configure(config):
    pathlib.Path("test-artifacts/videos").mkdir(parents=True, exist_ok=True)

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "test-artifacts/videos",
        "viewport": {"width": 1280, "height": 720},
    }