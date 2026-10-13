# Postman test plan

This project has no REST API server; Postman is used to inspect target HTTP responses.

1. Create a GET request to `https://quotes.toscrape.com/`.
2. Send it and inspect the status code, response headers, and HTML body.
3. Compare the response's `div.quote`, `span.text`, and `small.author` elements with the scraper's output.
4. For an approved API target, create requests using the API's documented endpoints and validate JSON keys and status codes.
5. Do not use Postman or the scraper to bypass authentication, CAPTCHAs, rate limits, or access restrictions.
