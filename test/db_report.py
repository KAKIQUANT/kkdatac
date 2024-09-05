import kkdatac
import pandas as pd


def generate_report():
    # Fetch all tables in the database
    databases_df = kkdatac.sql('show databases')
    tables_df = kkdatac.sql('show tables')

    report_data = []

    # Iterate through each table to fetch columns and data
    for table in tables_df['name']:  # Assuming the table names are in the 'name' column
        table_description_df = kkdatac.sql(f'DESCRIBE TABLE {table}')
        table_data_df = kkdatac.sql(f'SELECT * FROM {table} LIMIT 100')

        # Store the description and first 100 rows of data for each table
        report_data.append({
            'table': table,
            'columns': table_description_df,
            'sample_data': table_data_df
        })

    # Return all the gathered data
    return report_data


def generate_html_report(report_data):
    html = "<html><body><h1>Database Report</h1>"

    # Add content for each table
    for table_data in report_data:
        html += f"<h2>Table: {table_data['table']}</h2>"
        html += "<h3>Columns:</h3>"
        html += table_data['columns'].to_html(index=False)

        html += "<h3>Sample Data (First 100 rows):</h3>"
        html += table_data['sample_data'].to_html(index=False)

    html += "</body></html>"
    return html


# Generate the report data
report_data = generate_report()

# Convert the report data to HTML
html_report = generate_html_report(report_data)

# Save the HTML report
with open("report.html", "w") as file:
    file.write(html_report)

print("Report generated and saved as report.html")
