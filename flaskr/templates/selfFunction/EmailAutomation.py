#importing yagmail and its packages
import yagmail

#initiating connection with SMTP server
#SMTP= Simple Mail Transfer Protocol

yag = yagmail.SMTP("dougivevolunteer@gmail.com", "Enter your Email Password here")

try:
    yag.send(to = "dougivevolunteer@gmail.com", cc="qndlqrlyb@gmail.com", bcc="kandalker.liv@gmail.com",
    subject= "HTML Automation & Attachment Test", contents=["<h2> the test success </h2>", "<p> Yes!</p>"],
    attachments= [r"C:\Users\qndlq\PycharmProjects\pythonProject\flaskr\myPlot.png"])
    print("Email sent")

except:
    print("Error, Email not Send")