import asyncio
import kkdatac
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Thread pool executor for parallel tasks
executor = ThreadPoolExecutor(max_workers=10)


async def fetch_table_info(table):
    try:
        # Fetch table description and first 100 rows
        table_description = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(executor, kkdatac.sql, f'DESCRIBE TABLE {table}'), timeout=1000
        )
        table_data = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(executor, kkdatac.sql, f'SELECT * FROM {table} LIMIT 100'),
            timeout=1000
        )

        return {
            'table': table,
            'columns': table_description,
            'sample_data': table_data
        }
    except TimeoutError:
        return {
            'table': table,
            'error': 'Request timed out'
        }
    except Exception as e:
        return {
            'table': table,
            'error': str(e)
        }


async def generate_report():
    # Fetch the list of tables asynchronously
    tables_df = await asyncio.get_event_loop().run_in_executor(executor, kkdatac.sql, 'show tables')

    # Create a list of async tasks for fetching table info
    tasks = [fetch_table_info(table) for table in tables_df['name']]  # Assuming the table names are in 'name' column

    # Gather all the results
    report_data = await asyncio.gather(*tasks)
    return report_data


def generate_html_report(report_data):
    html = "<html><body><h1>Database Report</h1>"

    for table_data in report_data:
        if 'error' in table_data:
            html += f"<h2>Table: {table_data['table']}</h2>"
            html += f"<p><strong>Error:</strong> {table_data['error']}</p>"
        else:
            html += f"<h2>Table: {table_data['table']}</h2>"
            html += "<h3>Columns:</h3>"
            html += table_data['columns'].to_html(index=False)

            html += "<h3>Sample Data (First 100 rows):</h3>"
            html += table_data['sample_data'].to_html(index=False)

    html += "</body></html>"
    return html


async def main():
    # Generate the report data asynchronously
    report_data = await generate_report()

    # Convert the report data to HTML
    html_report = generate_html_report(report_data)

    # Save the HTML report
    with open("async_report.html", "w", encoding='utf-8') as file:
        file.write(html_report)

    print("Async report generated and saved as async_report.html")


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
