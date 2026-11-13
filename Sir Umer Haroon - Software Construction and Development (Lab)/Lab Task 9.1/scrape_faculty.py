"""Scrape IBA Karachi faculty profiles and save the submission files."""

import base64
import csv
import hashlib
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


FACULTY_URL = "https://www.iba.edu.pk/faculty-profiles.php"
OUTPUT_DIRECTORY = Path(__file__).parent
IMAGE_DIRECTORY = OUTPUT_DIRECTORY / "faculty_images"


def clean_text(value):
    return " ".join(value.split())


def safe_filename(value):
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "faculty"


def save_image(source, filename):
    if source.startswith("data:image/"):
        header, encoded_data = source.split(",", 1)
        extension = header.split("/")[1].split(";")[0].replace("jpeg", "jpg")
        image_path = IMAGE_DIRECTORY / f"{filename}.{extension}"
        image_path.write_bytes(base64.b64decode(encoded_data))
        return image_path.name

    image_path = IMAGE_DIRECTORY / f"{filename}.jpg"
    response = requests.get(urljoin(FACULTY_URL, source), timeout=30)
    response.raise_for_status()
    image_path.write_bytes(response.content)
    return image_path.name


def scrape_faculty():
    response = requests.get(FACULTY_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    IMAGE_DIRECTORY.mkdir(exist_ok=True)
    rows = []

    for card in soup.select(".faculty-profile-card"):
        details = card.select_one(".details")
        if details is None:
            continue
        name_tag = details.find("h4")
        designation_tag = details.find("p")
        profile_link = details.select_one("a[href*='faculty-profile.php']")
        if name_tag is None or designation_tag is None or profile_link is None:
            continue

        email_match = re.search(
            r"E-mail:\s*([^\s]+)",
            clean_text(details.get_text(" ", strip=True)),
            re.IGNORECASE,
        )
        image_tag = card.find("img")
        name = clean_text(name_tag.get_text())
        image_name = ""
        if image_tag and image_tag.get("src"):
            image_name = save_image(
                image_tag["src"],
                f"{safe_filename(name)}_{hashlib.sha1(name.encode()).hexdigest()[:8]}",
            )

        rows.append(
            {
                "Name": name,
                "Designation": clean_text(designation_tag.get_text()),
                "Department": "Not listed on the faculty directory",
                "Email": email_match.group(1) if email_match else "",
                "Contact": "Not listed",
            }
        )

    with (OUTPUT_DIRECTORY / "faculty_data.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Name", "Designation", "Department", "Email", "Contact"]
        )
        writer.writeheader()
        writer.writerows(rows)

    (OUTPUT_DIRECTORY / "university_info.txt").write_text(
        "University Name: Institute of Business Administration (IBA), Karachi\n"
        f"Faculty webpage URL: {FACULTY_URL}\n",
        encoding="utf-8",
    )
    print(f"Saved {len(rows)} faculty records and images to {OUTPUT_DIRECTORY}")


if __name__ == "__main__":
    scrape_faculty()
