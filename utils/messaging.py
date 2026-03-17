# utils/messaging.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS

def send_code(email, code, locker):
    """
    Envia o código do locker para o cliente por e-mail
    """
    if not email:
        print("Nenhum email fornecido!")
        return

    subject = "Seu código Ponto 24 para retirar a encomenda"
    html = f"""
    <html>
    <body style="font-family:Arial;background:#f5f6f7;padding:20px;">

    <div style="max-width:500px;margin:auto;background:white;border-radius:10px;overflow:hidden;box-shadow:0 5px 20px rgba(0,0,0,0.1);">

    <div style="background:#1f2933;color:white;padding:20px;text-align:center;">
    <h2 style="margin:0;color:#ff6a00;">PONTO 24</h2>
    <p style="margin:5px 0;">Rede Inteligente de Cacifos</p>
    </div>

    <div style="padding:30px;text-align:center;">

    <h3>Sua encomenda chegou!</h3>

    <p>Ela foi colocada em um locker seguro.</p>

    <div style="background:#f5f6f7;padding:20px;border-radius:8px;margin:20px 0;">

    <p><strong>Locker:</strong> {locker}</p>

    <p style="font-size:28px;
    letter-spacing:4px;
    color:#ff6a00;
    font-weight:bold;">
    {code}
    </p>

    <p style="font-size:12px;color:#777;">
    Use este código no terminal Ponto 24
    </p>

    </div>

    <p>Dirija-se ao terminal e insira o código para retirar sua encomenda.</p>

    </div>

    <div style="background:#f5f6f7;padding:15px;text-align:center;font-size:12px;color:#666;">
    Ponto 24 • Sua encomenda, Sempre perto • 24h
    </div>

    </div>

    </body>
    </html>
    """


    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    try:

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        print(f"[Email] Código {code} enviado para {email} no locker {locker}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")

def send_pickup_notice(email, locker):

    subject = "Encomenda retirada - Ponto 24"

    html = f"""
    <html>
    <body style="font-family:Arial;background:#f5f6f7;padding:20px;">

    <div style="max-width:500px;margin:auto;background:white;border-radius:10px;overflow:hidden;box-shadow:0 5px 20px rgba(0,0,0,0.1);">

    <div style="background:#1f2933;color:white;padding:20px;text-align:center;">
    <h2 style="margin:0;color:#ff6a00;">PONTO 24</h2>
    <p style="margin:5px 0;">Rede Inteligente de Cacifos</p>
    </div>

    <div style="padding:30px;text-align:center;">

    <h3>Encomenda retirada</h3>

    <p>Sua encomenda foi retirada com sucesso.</p>

    <p>Obrigado por usar o <strong>Ponto 24</strong>.</p>

    </div>

    <div style="background:#f5f6f7;padding:15px;text-align:center;font-size:12px;color:#666;">
    Ponto 24 • Sua encomenda, Sempre perto • 24h
    </div>

    </div>

    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()

        print(f"[Email] Confirmação de retirada enviada para {email}")

    except Exception as e:
        print(f"Erro ao enviar email de retirada: {e}")