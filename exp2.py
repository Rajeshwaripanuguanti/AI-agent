import gradio as gr
from transformers import pipeline
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os
import datetime
generator=pipeline("text-generation",model="tiiuae/falcon-rw-1b")
def generate_resume_text(name,phno,email,linkedIn_pro,skillset,achievments,qualification):
    prompt=f"""
            create a modern and professional resume
            Name:{name}
            phone no:{phno}
            email:{email}
            linkedIn Pro:{linkedIn_pro}
            skillset:{skillset}
            achievments:{achievments}
            qualification:{qualification}
            Focus on Data analyst with 3 year experience
            """
    result=generator(prompt,max_length=500,do_sample=True)
    return result[0]['generated_text']

def create_resume_pdf(name,generate_text):
    filename=f"{name.replace(' ',' ')}_resume.pdf" #rajeshwari_resume.pdf
    filepath=os.path.join(os.getcwd(),filename)
    c=canvas.Canvas(filepath,pagesize=A4)
    width,height=A4
    c.setFont("Helvetica-Bold",20)
    c.setFillColorRGB(0.2,0.4,0.6)
    c.drawCenteredString(width/2.0,height-80,f"{name}'s Resume")
    c.setFont("Helvetica",12)
    c.setFillColorRGB(0,0,0)
    lines=generate_resume_text.split('\n')
    y=height=120
    for line in lines:
        if y<50:
            c.showPage()
            y=height-50
        c.drawString(50,y,line.strip())
        y-=20
    c.save()
    return filepath

def send_mail(pdf_gen,email):
    sender_email="panuguantirajeshwari@gmail.com"
    password="lohs pixi fumi fobn"
    msg=MIMEMultipart()
    msg['subject']="Your auto-generated resume"
    msg["from"]=sender_email
    msg["To"]=email
    body=MIMEText("Hi,please your resume attached with mail")
    msg.attach(body)
    with open(pdf_gen,"rb") as f:
        part=MIMEApplication(f.read(),name=os.path.basename(pdf_gen))
        part['Content-Disposition']=f'attachment filename="{os.path.basename(pdf_path)}"'
        msg.attach(part)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
            server.login(sender_email,password)
            server.send_message(msg)
        return "Email sent successfully"
    except Exceptio as e:
        return f"Failed to send email:{str(e)}"
def agentic_resume(name,phno,email,linkedIn_pro,skillset,achievments,qualification):
    generate_text=generate_resume_text(name,phno,email,linkedIn_pro,skillset,achievments,qualification)
    pdf_gen=create_resume_pdf(name,generate_text)
    output=send_mail(pdf_gen,email)
    return f"Resume generated and saved as{pdf_path}{output}"

with gr.Blocks() as app:
    gr.Markdown("AI powered Resume builder and Mail")
    with gr.Row():
        name=gr.Textbox(label="Enter name")
        phno=gr.Textbox(label="Enter phno")
    with gr.Row():
        email=gr.Textbox(label="Enter email")
        linkedIn_pro=gr.Textbox(label="Enter linkedin profile")
    with gr.Row():
        achievments=gr.Textbox(label="Enter Achievments",lines=5)
        skillset=gr.Textbox(label="Enter skillset",lines=5)
    with gr.Row():
        qualification=gr.Textbox(label="Enter qualification")
        gen_button=gr.Button("Generate and send mail")
    with gr.Row():
        output=gr.Textbox(label="status/Info")
        file_output=gr.File(label="Download your resume")
    gen_button.click(agentic_resume,inputs=[name,phno,email,skillset,linkedIn_pro,qualification],outputs=[output,file_output])
app.launch()

