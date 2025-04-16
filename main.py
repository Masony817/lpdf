import os
from fpdf import FPDF
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_count():
    response = supabase.table("test").select("count").limit(1).execute()
    data = response.data
    if data and len(data) > 0:
        return data[0]["count"]
    return 0

def create_lpdf(filename: str):
    count = get_count()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    
    text = f"this count is at {count}"
    pdf.cell(200, 20, txt=text, ln=1, align="C")
    
    pdf.set_title("LPDF DEMO")
    pdf.set_author("LPDF by mason yarbrough")
    pdf.output(filename)
    print(f"PDF created: {filename}")
    
if __name__ == "__main__":
    create_lpdf("demo.lpdf")