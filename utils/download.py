import requests
from pathlib import Path

session_cookies = {
    2024: "53616c7465645f5f90610c22c367a30995b053f7543e3cee5f053dc5afcef9e4233d443bbc70013928880645f4767e419ddfd602ec495c07cc8ec10560149362",
}

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
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

if __name__ == "__main__":
    import sys
    download(*[int(_) for _ in sys.argv[1:]])
