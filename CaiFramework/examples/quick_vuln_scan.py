#!/usr/bin/env python3
"""
Quick Vulnerability Scanner - Análisis Rápido de Seguridad Web

Análisis directo de seguridad HTTP sin IA para resultados inmediatos.

Uso:
    python quick_vuln_scan.py <URL>
    python quick_vuln_scan.py https://example.com
"""

import argparse
import sys
import requests
from urllib.parse import urlparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Quick Vulnerability Scanner - Análisis Rápido de Seguridad'
    )
    parser.add_argument('url', help='URL a analizar (ej: https://example.com)')
    parser.add_argument(
        '--method',
        default='GET',
        choices=['GET', 'POST', 'PUT', 'DELETE'],
        help='Método HTTP (default: GET)'
    )
    return parser.parse_args()


def analyze_endpoint(url, method="GET"):
    """Analizar endpoint HTTP para vulnerabilidades de seguridad."""
    try:
        analysis = []
        analysis.append("\n=== HTTP ENDPOINT SECURITY ANALYSIS ===\n")

        # Analizar URL
        parsed_url = urlparse(url)
        analysis.append("🔍 URL ANALYSIS:")
        analysis.append(f"  • Protocol: {parsed_url.scheme}")
        if parsed_url.scheme != "https":
            analysis.append("    ⚠️  WARNING: Using insecure HTTP!")
        analysis.append(f"  • Domain: {parsed_url.netloc}")
        analysis.append(f"  • Path: {parsed_url.path}")
        if parsed_url.query:
            analysis.append(f"  • Query: {parsed_url.query}")

        # Request
        analysis.append(f"\n📤 REQUEST: {method} {url}")

        response = requests.request(
            method=method,
            url=url,
            verify=False,
            allow_redirects=True,
            timeout=10
        )

        # Response
        analysis.append(f"\n📥 RESPONSE:")
        analysis.append(f"  • Status: {response.status_code} {response.reason}")
        analysis.append(f"  • Size: {len(response.content):,} bytes")

        # Security Headers
        analysis.append("\n🔒 SECURITY ANALYSIS:\n")

        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME Sniffing Protection',
            'X-XSS-Protection': 'XSS Protection'
        }

        missing = []
        for header, desc in security_headers.items():
            if header not in response.headers:
                missing.append((header, desc))

        if missing:
            analysis.append("⚠️  MISSING SECURITY HEADERS:")
            for header, desc in missing:
                analysis.append(f"  • {header} ({desc})")
        else:
            analysis.append("✅ All critical security headers present")

        # Information Disclosure
        info_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version']
        disclosed = [(h, response.headers[h]) for h in info_headers if h in response.headers]

        if disclosed:
            analysis.append("\n⚠️  INFORMATION DISCLOSURE:")
            for header, value in disclosed:
                analysis.append(f"  • {header}: {value}")

        # Cookies
        if response.cookies:
            analysis.append("\n🍪 COOKIES:")
            for cookie in response.cookies:
                issues = []
                if not cookie.secure:
                    issues.append("Not Secure")
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    issues.append("Not HttpOnly")

                status = "⚠️ " if issues else "✅"
                analysis.append(f"  {status} {cookie.name}")
                if issues:
                    analysis.append(f"      Issues: {', '.join(issues)}")

        analysis.append("\n" + "="*50)

        return "\n".join(analysis)

    except requests.exceptions.Timeout:
        return f"❌ Timeout connecting to {url}"
    except requests.exceptions.ConnectionError:
        return f"❌ Could not connect to {url}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def main():
    args = parse_arguments()

    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "⚡ QUICK VULN SCAN ⚡" + " " * 37 + "║")
    print("║" + " " * 25 + "Fast Security Analysis" + " " * 31 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print(f"🎯 Target: {args.url}")
    print(f"📤 Method: {args.method}")
    print()
    print("─" * 80)

    # Ejecutar análisis
    result = analyze_endpoint(args.url, args.method)

    print(result)
    print()
    print("─" * 80)
    print("✅ Scan completed")
    print("─" * 80)
    print()
    print("💡 For AI-powered deep analysis:")
    print("   python examples/bug_bounty_hunter.py <URL> --no-guardrails")
    print()


if __name__ == "__main__":
    main()
