import smtplib
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('test.bot.9094@gmail.com','chirag1messi')
server.sendmail('test.bot.9094@gmail.com','chiragaftc@gmail.com','Mail is sent')
print("mail is sent")