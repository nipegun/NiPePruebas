"""
HTTP Analyzer Tool for Bug Bounty Hunting
"""
from urllib.parse import urlparse
import requests
from cai.sdk.agents import function_tool


@function_tool
async def analyze_http_endpoint(
    url: str,
    method: str = "GET"
) -> str:
    """
    Analyze an HTTP endpoint for security vulnerabilities and misconfigurations.

    This tool makes HTTP requests and performs comprehensive security analysis including:
    - URL structure analysis
    - Request/response header inspection
    - Security header validation
    - Detection of sensitive information exposure
    - Common vulnerability indicators

    Args:
        url: Target URL/endpoint to analyze (e.g., "https://example.com/api/users")
        method: HTTP method to use (GET, POST, PUT, DELETE, etc.). Default: GET

    Returns:
        Detailed security analysis report including vulnerabilities found

    Examples:
        - analyze_http_endpoint("https://example.com/api/users")
        - analyze_http_endpoint("https://api.example.com/login", method="POST")
        - analyze_http_endpoint("https://example.com/search")
    """
    try:
        analysis = []
        analysis.append("\n=== HTTP ENDPOINT SECURITY ANALYSIS ===\n")

        # Analyze URL structure
        parsed_url = urlparse(url)
        analysis.append("🔍 URL ANALYSIS:")
        analysis.append(f"  • Protocol: {parsed_url.scheme}")
        if parsed_url.scheme != "https":
            analysis.append("    ⚠️  WARNING: Using insecure HTTP instead of HTTPS!")
        analysis.append(f"  • Domain: {parsed_url.netloc}")
        analysis.append(f"  • Path: {parsed_url.path}")
        if parsed_url.query:
            analysis.append(f"  • Query Parameters: {parsed_url.query}")

        # Request details
        analysis.append(f"\n📤 REQUEST DETAILS:")
        analysis.append(f"  • Method: {method}")

        # Make the request
        analysis.append(f"\n⏳ Making {method} request to {url}...")

        response = requests.request(
            method=method,
            url=url,
            verify=False,  # For testing purposes
            allow_redirects=True,
            timeout=10
        )

        # Response analysis
        analysis.append("\n📥 RESPONSE ANALYSIS:")
        analysis.append(f"  • Status Code: {response.status_code}")

        status_emoji = "✅" if 200 <= response.status_code < 300 else "⚠️" if 300 <= response.status_code < 400 else "❌"
        analysis.append(f"    {status_emoji} {response.reason}")

        analysis.append(f"  • Response Size: {len(response.content):,} bytes")

        if response.history:
            analysis.append(f"  • Redirects: {len(response.history)} redirect(s)")
            for i, redir in enumerate(response.history, 1):
                analysis.append(f"    {i}. {redir.status_code} -> {redir.url}")

        # Response headers
        analysis.append("\n📋 RESPONSE HEADERS:")
        for header, value in response.headers.items():
            analysis.append(f"  • {header}: {value}")

        # Security analysis
        analysis.append("\n🔒 SECURITY ANALYSIS:\n")

        vulnerabilities = []
        recommendations = []

        # Check critical security headers
        security_headers = {
            'Strict-Transport-Security': 'HSTS - Forces HTTPS connections',
            'Content-Security-Policy': 'CSP - Prevents XSS and injection attacks',
            'X-Frame-Options': 'Clickjacking protection',
            'X-Content-Type-Options': 'MIME-sniffing protection',
            'X-XSS-Protection': 'XSS filter (legacy)',
            'Permissions-Policy': 'Controls browser features',
            'Referrer-Policy': 'Controls referrer information leakage'
        }

        missing_headers = []
        for header, description in security_headers.items():
            if header not in response.headers:
                missing_headers.append((header, description))

        if missing_headers:
            analysis.append("⚠️  MISSING SECURITY HEADERS:")
            for header, desc in missing_headers:
                analysis.append(f"  • {header}")
                analysis.append(f"    └─ {desc}")
                vulnerabilities.append(f"Missing security header: {header}")
                recommendations.append(f"Add {header} header")

        # Check for information disclosure
        info_disclosure_headers = [
            'Server', 'X-Powered-By', 'X-AspNet-Version',
            'X-AspNetMvc-Version', 'X-Generator'
        ]

        disclosed_info = []
        for header in info_disclosure_headers:
            if header in response.headers:
                disclosed_info.append((header, response.headers[header]))

        if disclosed_info:
            analysis.append("\n⚠️  INFORMATION DISCLOSURE:")
            for header, value in disclosed_info:
                analysis.append(f"  • {header}: {value}")
            vulnerabilities.append("Server/technology information disclosure")
            recommendations.append("Remove server/technology version headers")

        # Check response body for sensitive patterns
        body_lower = response.text.lower()
        sensitive_patterns = {
            'password': 'Password field in response',
            'api_key': 'API key exposure',
            'secret': 'Secret value exposure',
            'token': 'Token in response body',
            'private_key': 'Private key exposure',
            'access_token': 'Access token in response',
            'authorization': 'Authorization data in response'
        }

        found_sensitive = []
        for pattern, description in sensitive_patterns.items():
            if pattern in body_lower:
                found_sensitive.append((pattern, description))

        if found_sensitive:
            analysis.append("\n⚠️  POTENTIAL SENSITIVE DATA EXPOSURE:")
            for pattern, desc in found_sensitive:
                analysis.append(f"  • Found '{pattern}': {desc}")
                vulnerabilities.append(f"Sensitive data in response: {pattern}")

        # Check for common vulnerability indicators
        vuln_indicators = {
            'error': 'Error messages may leak information',
            'exception': 'Exception details exposed',
            'stack trace': 'Stack traces in response',
            'debug': 'Debug information exposed',
            'admin': 'Admin functionality accessible',
            'root': 'Root paths exposed',
            'sql': 'Potential SQL error messages'
        }

        found_indicators = []
        for indicator, desc in vuln_indicators.items():
            if indicator in body_lower:
                found_indicators.append((indicator, desc))

        if found_indicators:
            analysis.append("\n⚠️  VULNERABILITY INDICATORS:")
            for indicator, desc in found_indicators:
                analysis.append(f"  • '{indicator}' found: {desc}")

        # Check cookies
        if response.cookies:
            analysis.append("\n🍪 COOKIES ANALYSIS:")
            for cookie in response.cookies:
                analysis.append(f"  • {cookie.name}")
                issues = []
                if not cookie.secure:
                    issues.append("Not marked as Secure")
                    vulnerabilities.append(f"Cookie '{cookie.name}' not marked as Secure")
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    issues.append("Not marked as HttpOnly")
                    vulnerabilities.append(f"Cookie '{cookie.name}' not marked as HttpOnly")
                if not cookie.has_nonstandard_attr('SameSite'):
                    issues.append("No SameSite attribute")

                if issues:
                    analysis.append(f"    ⚠️  Issues: {', '.join(issues)}")

        # Summary
        analysis.append("\n" + "="*50)
        analysis.append("📊 VULNERABILITY SUMMARY:")

        if vulnerabilities:
            analysis.append(f"\n🔴 Found {len(vulnerabilities)} potential issue(s):")
            for i, vuln in enumerate(vulnerabilities, 1):
                analysis.append(f"  {i}. {vuln}")
        else:
            analysis.append("\n✅ No obvious vulnerabilities detected in initial scan")

        if recommendations:
            analysis.append(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                analysis.append(f"  {i}. {rec}")

        analysis.append("\n" + "="*50)
        analysis.append("\n⚠️  NOTE: This is an automated scan. Manual testing required for comprehensive assessment.")

        return "\n".join(analysis)

    except requests.exceptions.Timeout:
        return f"❌ Error: Request timeout after 10 seconds for {url}"
    except requests.exceptions.ConnectionError:
        return f"❌ Error: Could not connect to {url}. Check if the server is accessible."
    except requests.exceptions.TooManyRedirects:
        return f"❌ Error: Too many redirects when accessing {url}"
    except Exception as e:
        return f"❌ Error analyzing endpoint: {str(e)}"
