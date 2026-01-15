# Vulnerable Website for Penetration Testing

This is a deliberately vulnerable website created for educational penetration testing purposes. It contains common web vulnerabilities such as SQL injection, XSS, CSRF, and insecure file uploads.

## Vulnerabilities Included

- **SQL Injection**: In the login form, user input is directly concatenated into SQL queries.
- **Cross-Site Scripting (XSS)**: Search results display user input without sanitization.
- **Cross-Site Request Forgery (CSRF)**: Forms lack CSRF tokens.
- **Insecure File Upload**: Files can be uploaded without validation.
- **Directory Traversal**: The `/file` endpoint allows accessing files outside the intended directory.
- **Insecure Session Management**: Secret key is hardcoded and insecure.

## Setup

1. Install dependencies:
   ``` 
  pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python app.py
   ```

3. Open your browser and go to `http://localhost:5000`

## Features

- User authentication with session management
- Product catalog with real images
- Product detail pages with images
- Checkout system with payment simulation
- Search functionality for cars (vulnerable to SQL injection)
- Video embeds
- Similar vehicles section
- Admin panel for user management
- File upload (no validation)
- Directory traversal vulnerability

## Usage

- Login with username `admin` and password `password` (or `user`/`pass`, or `adomin`/`adominpass`).
- Browse car listings in the dashboard with images, videos, and similar vehicles.
- Search for cars by name.
- Click on a car to view details and buy.
- Use "Buy Now" to proceed to checkout.
- Test for vulnerabilities using tools like Burp Suite, sqlmap, etc.

## Disclaimer

This website is for educational purposes only. Do not use it in production or for malicious activities. Always obtain permission before conducting penetration tests.

## Troubleshooting

- Ensure Python 3 is installed.
- If port 5000 is in use, change the port in `app.py`.
- Database is stored in `vulnerable.db`; delete it to reset.