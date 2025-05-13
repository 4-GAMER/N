import re

def markdown_to_html(md_text):
    html_output = []
    in_ul = False
    # Skip the first H1 if it's the main title, as it's already in the HTML header
    lines = md_text.split('\n')
    start_index = 0
    if lines[0].startswith('# '):
        start_index = 1 # Skip the first line if it's H1
        # We might want to add the content of H1 as a paragraph or ensure it's not duplicated
        # For now, let's just skip it from the main content section generation

    for i in range(start_index, len(lines)):
        line = lines[i]
        # Handle multiple blank lines between sections by only processing non-empty lines after stripping
        stripped_line = line.strip()

        if not stripped_line:
            if in_ul:
                html_output.append('</ul>')
                in_ul = False
            # Add a line break or spacer if needed for visual separation, or let CSS handle margins
            # html_output.append('<br>') # Optional: for visual spacing if CSS margins aren't enough
            continue

        # Headings
        if stripped_line.startswith('### '):
            if in_ul: html_output.append('</ul>'); in_ul = False
            html_output.append(f"<h3>{stripped_line[4:]}</h3>")
        elif stripped_line.startswith('## '):
            if in_ul: html_output.append('</ul>'); in_ul = False
            html_output.append(f"<h2>{stripped_line[3:]}</h2>")
        # Unordered lists
        elif stripped_line.startswith('*   '):
            if not in_ul:
                html_output.append('<ul>')
                in_ul = True
            processed_item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', stripped_line[4:])
            html_output.append(f"<li>{processed_item}</li>")
        elif stripped_line.startswith('* '):
            if not in_ul:
                html_output.append('<ul>')
                in_ul = True
            processed_item = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', stripped_line[2:])
            html_output.append(f"<li>{processed_item}</li>")
        # Paragraphs
        else:
            if in_ul:
                html_output.append('</ul>')
                in_ul = False
            processed_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', stripped_line)
            # Handle specific patterns like (تاريخ النشر التقريبي: ...)
            if processed_line.startswith('(') and processed_line.endswith(')'):
                 html_output.append(f'<p class="meta-info">{processed_line}</p>')
            else:
                html_output.append(f"<p>{processed_line}</p>")

    if in_ul: # Close any unclosed ul
        html_output.append('</ul>')

    return '\n'.join(html_output)

# Read Markdown file
with open("/home/ubuntu/video_analysis/final_report.md", "r", encoding="utf-8") as f:
    markdown_content = f.read()

# Convert to HTML
html_content_to_insert = markdown_to_html(markdown_content)

# Read index.html
with open("/home/ubuntu/telegraph_style_page/index.html", "r", encoding="utf-8") as f:
    index_html_content = f.read()

# Replace placeholder
placeholder = "<!-- سيتم إدراج محتوى التقرير هنا لاحقًا -->"
updated_index_html_content = index_html_content.replace(placeholder, html_content_to_insert)

# Write updated index.html
with open("/home/ubuntu/telegraph_style_page/index.html", "w", encoding="utf-8") as f:
    f.write(updated_index_html_content)

print("HTML page populated successfully.")

