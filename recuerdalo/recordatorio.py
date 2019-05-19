import smtplib, ssl
import datetime
import conf

def send_email( subject, content ):
    for ill in [ "\n", "\r" ]:
        subject = subject.replace(ill, ' ')

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'From': conf.sender,
        'To': conf.to,
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
        'X-Mailer': 'python',
        'Subject': subject
    }

    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    msg += "\n%s\n"  % (content)

    context = ssl.create_default_context()
    s = smtplib.SMTP_SSL(conf.host, conf.port, context=context)

    if conf.tls:
        s.ehlo()
        s.starttls()
        s.ehlo()

    if conf.username and conf.password:
        s.login(conf.username, conf.password)

    print ("sending %s to %s" % (subject, headers['To']))
    s.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
    s.quit()

