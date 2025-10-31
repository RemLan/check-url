# Check URL Redirects and Status

This Python script `check_urls.py` is designed to read a list of URLs from a CSV file, check their HTTP status, follow redirects, and report the final URL and any errors encountered. It's useful for verifying the accessibility and correct redirection of a large number of URLs.

## Features

*   Reads URLs from a semicolon-separated CSV file.
*   Performs HTTP GET requests to each URL.
*   Follows HTTP redirects (3xx status codes) and captures the final URL.
*   Reports HTTP status codes (2xx, 3xx, 4xx, 5xx).
*   Provides detailed error descriptions for connection issues, HTTP errors, and unknown errors.
*   Includes a bypass for SSL certificate verification to handle common certificate issues during checks.
*   Outputs results to a new CSV file with added error and final URL information.

## Setup

1.  **Python:** Ensure you have Python 3 installed on your system.
2.  **Dependencies:** This script uses standard Python libraries (`csv`, `sys`, `os`, `time`, `urllib.request`, `urllib.error`, `ssl`), so no additional `pip` installations are required.

## Usage

1.  **Prepare your Input CSV:**
    *   Create a CSV file (e.g., `urls.csv`) in the `input/` directory.
    *   The CSV file should be semicolon-separated.
    *   The first row is expected to be a header.
    *   Each subsequent row should contain at least two columns: `SKU` and `URL`.
    *   Example `input/urls.csv`:
        ```csv
        SKU;URL
        10287664;https://www.nexans.es/.rest/redirect/v1/product/10287664
        10287665;https://www.nexans.es/.rest/redirect/v1/product/10287665
        ```

2.  **Run the script:**
    Open your terminal or command prompt, navigate to the project directory, and run the script with your input CSV file as an argument:

    ```bash
    python3 check_urls.py your_input_file.csv
    ```
    Replace `your_input_file.csv` with the actual name of your CSV file located in the `input/` directory.

    Example:
    ```bash
    python3 check_urls.py URL\ Deeplinks\ produit\ pour\ test\(Export\).csv
    ```

## Output

The script will generate a new CSV file in the `output/` directory. The output filename will be `your_input_file_result.csv`.

The output CSV will include all original columns from your input file, plus three new columns: `Error`, `Error code`, and `Final URL`.

### Output Columns Explained:

*   **Error**: A descriptive message indicating the outcome of the URL check.
    *   `Success`: The URL returned a 2xx status code.
    *   `Redirect Success`: The URL redirected successfully (3xx status code), and the final destination was reached.
    *   `HTTP Error {code}`: An HTTP error occurred (e.g., `HTTP Error 404` for Not Found, `HTTP Error 500` for Internal Server Error).
    *   `Connection Error`: A network-related issue prevented connection (e.g., DNS resolution failure, timeout, SSL certificate issue).
    *   `Unknown Error`: Any other unexpected error.
*   **Error code**: The specific HTTP status code (e.g., `200`, `301`, `404`) or a detailed reason for connection errors (e.g., `[SSL: CERTIFICATE_VERIFY_FAILED]`, `[Errno 60] Connection timed out`).
*   **Final URL**: The URL after all redirects have been followed. If no redirects occurred, this will be the original URL.

## Example Output

```csv
SKU;URL;Error;Error code;Final URL
10287664;https://www.nexans.es/.rest/redirect/v1/product/10287664;Success;200;https://www.nexans.es/en/products/Renewables/Solar/Nexans-PV-38188/product~10287664~.html
10287665;https://www.nexans.es/.rest/redirect/v1/product/10287665;HTTP Error;404;https://www.nexans.es/.rest/redirect/v1/product/10287665
