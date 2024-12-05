import requests
from pathlib import Path
from .session_cookies import session_cookies

def download(day, year=2024):
    # URL of the text document
    url = f"https://adventofcode.com/{year}/day/{day}/input"

    # Create a session
    session = requests.Session()

    # Set the session cookie
    session.cookies.set("session", session_cookies[year])

    # Make a request to download the document
    response = session.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content to a file
        Path(f"day{day}.txt").write_text(response.text)
        print(f"{url} downloaded")
        print("Line1:", response.text.splitlines()[0])
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

if __name__ == "__main__":
    import sys
    download(*[int(_) for _ in sys.argv[1:]])
