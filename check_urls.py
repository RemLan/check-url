import csv
import sys
import os
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import ssl

if len(sys.argv) != 2:
    print("Usage: python3 check_urls.py <filename.csv>")
    sys.exit(1)

filename = sys.argv[1]
input_path = os.path.join('input', filename)
if not os.path.exists(input_path):
    print(f"File {input_path} not found.")
    sys.exit(1)

output_filename = os.path.splitext(filename)[0] + '_result.csv'
output_path = os.path.join('output', output_filename)

with open(input_path, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter=';')
    rows = list(reader)

header = rows[0] + ['Error', 'Error code', 'Final URL']
results = [header]

for row in rows[1:]:
    if len(row) < 2:
        results.append(row + ['Invalid row', ''])
        continue

    sku = row[0]
    url = row[1].strip()
    if not url:
        results.append(row + ['No URL', ''])
        continue

    error_desc = ''
    error_code = ''
    final_url = url # Initialize final_url with the original URL
    try:
        req = Request(url, method='GET')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        print(f"req: {req.__class__.__name__}")
        # Create an unverified SSL context to bypass certificate verification
        context = ssl._create_unverified_context()
        with urlopen(req, timeout=11, context=context) as response:
            status = response.getcode()
            final_url = response.geturl() # Get the final URL after potential redirects
            print(f"response: {status}")
            print(f"Status:  {str(status)}")
            error_code = str(status)
            if 200 <= status < 300:
                error_desc = 'Success'
            elif 300 <= status < 400:
                error_desc = 'Redirect Success'
            else:
                error_desc = f'HTTP Error {status}'
    except HTTPError as e:
        if 300 <= e.code < 400:
            error_code = str(e.code)
            error_desc = 'Redirect Success'
        else:
            error_code = str(e.code)
            error_desc = f'HTTP Error {e.code}'
    except URLError as e:
        error_desc = 'Connection Error'
        error_code = str(e.reason) if hasattr(e, 'reason') else 'Connection failed'
    except Exception as e:
        error_desc = 'Unknown Error'
        error_code = str(e)

    results.append(row + [error_desc, error_code, final_url])
    print(f"Processing SKU: {sku} - URL: {url} - Error: {error_desc} (Code: {error_code}) - Final URL: {final_url}")
    time.sleep(0.5)  # Delay to avoid overwhelming the server

with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter=';')
    writer.writerows(results)

print(f"Output written to {output_path}")
