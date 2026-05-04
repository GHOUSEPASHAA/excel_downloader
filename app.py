from flask import Flask, send_file
import pandas as pd
import pyodbc
import io
import os   # ✅ FIX

app = Flask(__name__)

@app.route('/export')
def export_excel():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=server-jack.database.windows.net;"
            "DATABASE=azure-sql-dataflow;"
            f"UID={os.environ.get('DB_USER')};"
            f"PWD={os.environ.get('DB_PASS')};"   # ✅ FIXED
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
            "Connection Timeout=30;"
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
