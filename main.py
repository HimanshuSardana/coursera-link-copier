from tkinter import Tk  # in Python 2, use "Tkinter" instead

r = Tk()
import os
from cerebras.cloud.sdk import Cerebras
import sys

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

if len(sys.argv) > 1:
    pass
else:
    print("Usage: python main.py <course_name>")
    sys.exit(1)

COURSE_NAME = str(sys.argv[1]) if len(sys.argv) > 1 else "Data Science 101"

PROMPT = f"""
Write a Linkedin post about me completing the {COURSE_NAME} course.
Make it sound exciting and engaging, include stuff that I learned.
Keep it short and concise. Do not include any emojis or em-dashes.

DO NOT INCLUDE ANYTHING ELSE, JUST THE LINKEDIN POST.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": PROMPT,
        }
    ],
    model="llama-3.3-70b",
)

HASHTAGS = """
#TIET
#ThaparUniversity
#ThaparOutcomeBasedLearning
#ThaparCoursera
#Coursera
#UCS654_Predictive_Analytics
"""

print(chat_completion.choices[0].message.content + "\n\n" + HASHTAGS)
