import pandas as pd

def csv_to_html(csv_file="", header_title=""):
    # Load the CSV file Replace with your CSV file path
    df = pd.read_csv(f"{csv_file}.csv", encoding="utf-8", low_memory=False, dtype=str)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.fillna('')
    html_table = df.to_html(index=False, border=0, classes='table table-striped', escape=False)
    # Wrap the HTML table in a basic HTML structure
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV to HTML Table</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            table {{
                width: 50%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 4px;
                text-align: left;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>{header_title}</h2>
            {html_table}
        </div>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(f'{csv_file}.html', 'w') as f:
        f.write(html_content)

    print("HTML file created successfully!")