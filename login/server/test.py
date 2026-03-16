import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Test with port 465 (SSL)
def test_port_465():
    print("\n=== Testing Port 465 (SSL) ===")
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=30)
        server.login("vasukijoshi02@gmail.com", "alfhxelinyrcpwky")
        
        msg = MIMEText("Test from VPS - Port 465")
        msg['Subject'] = 'VPS Test 465'
        msg['From'] = "vasukijoshi02@gmail.com"
        msg['To'] = "spoorthijoshi2003@gmail.com"
        
        server.sendmail("vasukijoshi02@gmail.com", "spoorthijoshi2003@gmail.com", msg.as_string())
        server.quit()
        print("✅ Port 465 SUCCESS!")
        return True
    except Exception as e:
        print(f"❌ Port 465 FAILED: {type(e).__name__}: {e}")
        return False

# Test with port 587 (TLS)
def test_port_587():
    print("\n=== Testing Port 587 (TLS) ===")
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        server.starttls(context=context)
        server.login("vasukijoshi02@gmail.com", "alfhxelinyrcpwky")
        
        msg = MIMEText("Test from VPS - Port 587")
        msg['Subject'] = 'VPS Test 587'
        msg['From'] = "vasukijoshi02@gmail.com"
        msg['To'] = "spoorthijoshi2003@gmail.com"
        
        server.sendmail("vasukijoshi02@gmail.com", "spoorthijoshi2003@gmail.com", msg.as_string())
        server.quit()
        print("✅ Port 587 SUCCESS!")
        return True
    except Exception as e:
        print(f"❌ Port 587 FAILED: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("Testing SMTP from VPS...")
    
    result_465 = test_port_465()
    result_587 = test_port_587()
    
    print("\n=== RESULTS ===")
    print(f"Port 465 (SSL): {'✅ WORKS' if result_465 else '❌ BLOCKED'}")
    print(f"Port 587 (TLS): {'✅ WORKS' if result_587 else '❌ BLOCKED'}")
    
    if result_465:
        print("\n✅ USE PORT 465 - Update .env: SMTP_PORT=465")
    elif result_587:
        print("\n✅ USE PORT 587 - Keep current settings")
    else:
        print("\n❌ BOTH PORTS BLOCKED - Contact VPS provider or use SendGrid/AWS SES")
