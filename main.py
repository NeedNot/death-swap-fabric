from PIL import Image, ImageDraw, ImageFont
import os
import webbrowser
import subprocess
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


with open('options.json', 'r') as f:
    options = f.read()
options = json.loads(options)

file = open("questions.txt", "r")

lines = 0
for line in file:
  line = line.strip("\n")

  words = line.split()
  lines += 1

file.close()

px = (lines * 45) + 69

sender_email = options['email']['address']
receiver_email = input("Send email to: ")
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
password = options['email']['password']

message = MIMEMultipart("alternative")
message["Subject"] = options['email']['subject']
message["From"] = sender_email
message["To"] = receiver_email
filename = options['filename']
url = options['url']
main = f'<p><img src="{url}{filename}" alt="" width="497" height="{px}" /></p>'
# Create the plain-text and HTML version of your message
html = ("""
<html>
  <body>
    {main}
  </body>
</html>
""").replace("{main}", main)

# Turn these into plain/html MIMEText objects
part1 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

page = ""

with open('questions.txt', 'r') as f:
    questions = f.read().splitlines()

for question in questions:
    answer = input(question+" ")
    page = f"{page}{question}\n{answer}\n\n"

# name of the file to save

path = options['path']

fnt = ImageFont.truetype('arial.ttf', 12)

# create new image
image = Image.new(mode = "RGB", size = (497,px), color = "white")
draw = ImageDraw.Draw(image)
draw.text((2,10), page, font=fnt, fill=(0,0,0))
# save the file
image.save(f"{path}/{filename}")


os.chdir(f"{path}")
os.system("git add .")
os.system('git commit -m "image"')
os.system("git push origin master")

webbrowser.open(f'{url}{filename}', new=2)

print("Done! Check for errors")
input()
