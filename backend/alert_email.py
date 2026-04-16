

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ── YOUR GMAIL CONFIG ──────────────────────────────────────────────────────
# Use an App Password (not your real Gmail password).
# Steps: Google Account → Security → 2-Step Verification → App passwords
SENDER_EMAIL    = "varadavarada088@gmail.com"
SENDER_PASSWORD = "xceu oxcu cvhi jszf"   # ← replace with 16-char App Password
# ──────────────────────────────────────────────────────────────────────────


def send_intruder_alert(to_email: str, username: str) -> bool:
    """
    Sends an HTML + plain-text intruder-alert email.
    Returns True on success, False on failure.
    """
    now = datetime.now().strftime("%d %b %Y, %H:%M:%S")

    subject = "🚨 Security Alert: Suspicious Activity on Your Account"

    plain_body = f"""
Dear {username},

We detected suspicious activity on your account at {now}.

An unrecognised behaviour pattern was identified during your active session.
Your session has been terminated as a precaution.

If this was NOT you:
  • Change your password immediately
  • Review recent account activity
  • Enable two-factor authentication if available

If this WAS you (e.g. you changed how you were typing or using a different
device), simply log in again — the system will re-learn your pattern.

────────────────────────────────
This is an automated alert from your Adaptive Authentication System.
Do not reply to this email.
"""

    html_body = f"""
<html>
<body style="font-family:'Segoe UI',sans-serif;background:#f4f4f8;padding:30px;">
  <div style="max-width:520px;margin:auto;background:white;border-radius:14px;
              box-shadow:0 4px 20px rgba(0,0,0,0.08);overflow:hidden;">

    <!-- header -->
    <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                padding:28px 30px;color:white;text-align:center;">
      <h1 style="margin:0;font-size:1.4rem;">🚨 Security Alert</h1>
      <p style="margin:6px 0 0;opacity:.85;font-size:.9rem;">
        Adaptive Authentication System
      </p>
    </div>

    <!-- body -->
    <div style="padding:28px 30px;color:#333;">
      <p>Dear <strong>{username}</strong>,</p>
      <p>We detected <strong>suspicious behaviour</strong> on your account and
         terminated the session at:</p>

      <div style="background:#fef3f3;border-left:4px solid #e53e3e;
                  border-radius:6px;padding:12px 16px;margin:16px 0;
                  font-weight:600;color:#c53030;">
        🕐 {now}
      </div>

      <p>Our behavioural biometrics engine identified a pattern that did not
         match your registered profile. This may mean someone else gained
         access to your session.</p>

      <h3 style="color:#764ba2;margin-top:24px;">What you should do</h3>
      <ul style="padding-left:20px;line-height:1.9;">
        <li>Change your password immediately</li>
        <li>Review recent account activity</li>
        <li>Log back in — the system will verify your identity again</li>
      </ul>

      <p style="margin-top:20px;font-size:.85rem;color:#888;">
        If this alert was triggered by mistake (e.g. you were typing unusually
        or on a different device), simply log in again. The system continuously
        adapts to legitimate changes in your behaviour over time.
      </p>
    </div>

    <!-- footer -->
    <div style="background:#f7f8fc;padding:16px 30px;text-align:center;
                font-size:.78rem;color:#aaa;border-top:1px solid #eee;">
      Automated message · Do not reply · Adaptive Authentication System
    </div>
  </div>
</body>
</html>
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = to_email

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body,  "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"[📧] Alert sent → {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[❌] Email auth failed — check SENDER_PASSWORD (use App Password!)")
        return False

    except Exception as e:
        print(f"[❌] Email error: {e}")
        return False
