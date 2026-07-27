# 🐜 ANT DEV API COMPRESSION CHECK

## Goal

Keep ANT CLAW network responses fast and efficient.

## Client Negotiation

Client should request:

```
Accept-Encoding: gzip, br
```

## Server / Edge Rules

Enable:

- Brotli compression
- Gzip compression

Use compression threshold:

```
Only compress responses above small payload size.
Example: > 1 KB
```

## Do Not Compress

Skip already compressed content:

- images
- videos
- zip files
- APK files
- gzip files
- other binary compressed payloads

## Verification

Check response headers:

```
Content-Encoding: br
```

or

```
Content-Encoding: gzip
```

Check:

- Transfer size reduction
- JSON still parses correctly
- No double compression
- No API failures

## ANT DEV REPORT

```
🐜 ANT DEV UPDATE

Compression:

Checked:

Changed:

Measured:

Test:

Status:
```
