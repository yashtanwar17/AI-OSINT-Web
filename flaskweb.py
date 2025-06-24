from flask import Flask, render_template_string, Markup

app = Flask(__name__)

def parse_report_to_html(report_text):
    lines = report_text.splitlines()
    html = []
    current_section = ""

    for line in lines:
        line = line.strip()

        if line.startswith("### "):
            # Big Section Header
            html.append(f"<h2>{line[4:].strip()}</h2>")
        elif line.startswith("#### "):
            # Subsection Header
            html.append(f"<h3>{line[5:].strip()}</h3>")
        elif line.startswith("- **") or line.startswith("* **"):
            # Bullet with bold title
            line = line.replace("**", "<b>").replace("**", "</b>", 1)
            html.append(f"<li>{line}</li>")
        elif line.startswith("- "):
            html.append(f"<li>{line[2:].strip()}</li>")
        elif line.startswith("**") and line.endswith("**"):
            # Bold paragraph heading
            html.append(f"<p><b>{line.strip('*')}</b></p>")
        elif line.startswith("---"):
            html.append("<hr>")
        elif line:
            html.append(f"<p>{line}</p>")

    return Markup("\n".join(html))

# Load AI-reviewed report
def load_report():
    try:
        with open("ailog.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "No report available yet. Please upload log.txt and generate a report."

@app.route("/")
def home():
    report = load_report()
    formatted_html = parse_report_to_html(report)
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Web Scanner AI Report</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f5f5f5; color: #222; padding: 2em; max-width: 900px; margin: auto; }
            h1 { color: #0d6efd; }
            h2 { color: #0d6efd; margin-top: 1.5em; }
            h3 { color: #198754; margin-top: 1em; }
            li { margin-bottom: 0.4em; }
            p { margin: 0.6em 0; }
            hr { margin: 2em 0; border: 1px solid #ccc; }
            .report-box { background: white; padding: 2em; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="report-box">
            <h1>🔍 Web Security AI Report</h1>
            {{ formatted_html | safe }}
        </div>
    </body>
    </html>
    """, formatted_html=formatted_html)

if __name__ == "__main__":
    app.run(debug=True)
