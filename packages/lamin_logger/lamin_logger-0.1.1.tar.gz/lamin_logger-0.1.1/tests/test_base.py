from lamin_logger import logger


def test_logger():
    assert logger.level("INFO").name == "INFO"
