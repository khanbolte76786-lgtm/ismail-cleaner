import os, fitz
from pyrogram import Client, filters

# --- ISMAIL CONFIG ---
API_ID = 31493818
API_HASH = "27ebb6f386115ed9cda297c94d585390"
BOT_TOKEN = "8327858239:AAEJrJ1-KrvA4iSWiq6apnrc2Aq2ag0D2UU"

app = Client("IsmailCleaner", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document)
async def clean_pdf(c, m):
    if not m.document.file_name.endswith(".pdf"): return
    status = await m.reply("⏳ Cleaning... please wait.")
    file_path = await m.download()
    output_path = f"Cleaned_{m.document.file_name}"
    try:
        doc = fitz.open(file_path)
        for page in doc:
            for target in ["OceanofPDF.com", "OceanofPDF"]:
                for inst in page.search_for(target):
                    page.add_redact_annotation(inst, fill=(1, 1, 1))
                    page.apply_redactions()
                    page.insert_text(inst[:2], "t.me/silentlibrarypdfs", color=(0,0,1), fontsize=8)
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()
        await m.reply_document(output_path, caption="✅ Cleaned by Ismail's Bot!")
        os.remove(file_path); os.remove(output_path)
    except Exception as e:
        await m.reply(f"❌ Error: {e}")
    await status.delete()

app.run()
