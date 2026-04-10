from bs4 import BeautifulSoup
import pandas as pd

# Load HTML file
file_path = "/Users/radenn/Documents/Scraper/today.txt"
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")
customer_blocks = soup.find_all("div", class_="private-sea-tab-customer-profile")

data = []

for block in customer_blocks:
    # Member ID
    member_span = block.find("span", class_="member-id")
    member_id = member_span.get_text(strip=True) if member_span else ""

    # Company Name
    company_tag = block.find("div", class_="private-sea-tab-customer-profile-head-title").find("a")
    company_name = company_tag.get_text(strip=True) if company_tag else ""

    # Body kiri
    contact_block = block.find("div", class_="private-sea-tab-customer-profile-body-left")

    # Contact Name
    contact_name = ""
    if contact_block:
        divs = contact_block.find_all("div")
        for div in divs:
            label = div.find("span")
            if label and "Primary Contact" in label.get_text():
                contact_name = div.get_text(strip=True).replace("Primary Contact", "").strip()
                break

    # Phone Number
    phone_div = contact_block.find("div", class_="verify-line") if contact_block else None
    phone_number = phone_div.get_text(strip=True) if phone_div else ""

    # Email
    email_span = None
    if contact_block:
        email_span = contact_block.select_one(".ggs-verify-tag-wrap span")
    email = email_span.get_text(strip=True) if email_span else ""

    # Intent Grade
    intent_grade = ""
    if contact_block:
        intent_spans = contact_block.find_all("span")
        for idx, span in enumerate(intent_spans):
            if "Intend Grade" in span.get_text():
                if idx + 1 < len(intent_spans):
                    intent_grade = intent_spans[idx + 1].get_text(strip=True)
                break

    # Notes (ambil dari tab Notes, bukan Customer Activities)
    note_text = ""
    tabpanes = block.select("div.next-tabs-tabpane")
    for tab in tabpanes:
        note_span = tab.select_one("p > span.desc-detail")
        if note_span:
            note_text = note_span.get_text(strip=True)
            break  # hanya ambil notes pertama yang ditemukan

    # Tambahkan ke data list
    data.append({
        "Member ID": member_id,
        "Company Name": company_name,
        "empty_1": "",
        "Primary Contact Tel": phone_number,
        "Primary Contact Mailbox": email,
        "empty_2": "",
        "Primary Contact Name": contact_name,
        "Intent Grade": intent_grade,
        "empty_3": "",
        "empty_4": "",
        "empty_5": "",
        "empty_6": "",
        "Notes": note_text
    })

# Simpan ke Excel
df = pd.DataFrame(data)
output_path = "/Users/radenn/Documents/Scraper/today.xlsx"
df.to_excel(output_path, index=False)

print("✅ File berhasil dibuat di:", output_path)
