import sqlite3
import re
import time
from playwright.sync_api import sync_playwright

URL = "https://www.coursera.org/programs/data-science-elective-basket-2025-27-t7q2l/my-learning?myLearningTab=COMPLETED"
USER_DATA_DIR = "/home/himanshu/.config/chromium"


def extract_cert_links(html):
    pattern = r'href="(/account/accomplishments/records/[A-Z0-9]+)"'
    return re.findall(pattern, html)


def extract_course_titles(html):
    pattern = r'class="course-logo"[^>]*alt="([^"]+)"'
    return re.findall(pattern, html)


def get_page_html(url):
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            executable_path="/usr/bin/chromium",
        )

        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")

        while True:
            try:
                view_more_button = page.query_selector("button:has-text('View More')")
                if view_more_button:
                    view_more_button.click()
                    page.wait_for_load_state("networkidle")
                    time.sleep(2)
                else:
                    break
            except Exception as e:
                print(f"Error clicking 'View More' button: {e}")
                break

        html = page.content()
        context.close()
        return html


if __name__ == "__main__":
    html = get_page_html(URL)
    course_titles = extract_course_titles(html)
    cert_links = extract_cert_links(html)

    dict_courses = {}
    for title, link in zip(course_titles, cert_links):
        dict_courses[title] = f"https://www.coursera.org{link}"
    print(dict_courses)

con = sqlite3.connect("courses.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, cert_link TEXT, posted BOOLEAN DEFAULT 0, UNIQUE(title))"
)
for title, cert_link in dict_courses.items():
    try:
        cur.execute(
            "INSERT INTO courses (title, cert_link) VALUES (?, ?)", (title, cert_link)
        )
    except sqlite3.IntegrityError:
        print(f"Course '{title}' already exists in the database.")
con.commit()
con.close()
