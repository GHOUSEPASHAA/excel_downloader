from flask import Flask, send_file
import pandas as pd
import pymssql
import io
import os   # ✅ FIX

app = Flask(__name__)

@app.route('/export')
def export_excel():
    try:
        conn = pymssql.connect(
    server='server-jack.database.windows.net',
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    database='azure-sql-dataflow'
)

        df = pd.read_sql("SELECT * FROM Customers", conn)
        conn.close()

        if df.empty:
            return "No data found"

        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(output,
                         download_name="data.xlsx",
                         as_attachment=True)

    except Exception as e:
        return str(e)

# ✅ REQUIRED FOR RENDER
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
