import re

def extract_score(text):

    patterns = [
        r"Overall Score[:\s]*(\d+)",
        r"Overall Score.*?(\d+)/10",
        r"Score[:\s]*(\d+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return 0