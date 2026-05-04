"""Render Excalidraw JSON to PNG via the local mcp_excalidraw canvas server.

Usage:
    python render_excalidraw.py <path-to-file.excalidraw> [--output path.png] [--scale 2]

Requirements:
    - Canvas server running: cd ~/Dev/mcp_excalidraw && PORT=3000 npm run canvas
    - Browser tab open at http://localhost:3000  (or --headless flag to auto-open)

The --headless flag launches Playwright to open localhost:3000 automatically
so the export works without a manual browser window.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
import time
from pathlib import Path


CANVAS_URL = "http://localhost:3000"


def check_server() -> dict | None:
    try:
        import urllib.request
        with urllib.request.urlopen(f"{CANVAS_URL}/health", timeout=5) as r:
            return json.loads(r.read())
    except Exception:
        return None


def post_json(path: str, payload: dict) -> dict:
    import urllib.request
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{CANVAS_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=35) as r:
        return json.loads(r.read())


def render(excalidraw_path: Path, output_path: Path | None, scale: int, headless: bool) -> Path:
    # Load and validate the .excalidraw file
    data = json.loads(excalidraw_path.read_text(encoding="utf-8"))
    if data.get("type") != "excalidraw":
        print("ERROR: Not a valid .excalidraw file.", file=sys.stderr)
        sys.exit(1)

    elements = [e for e in data.get("elements", []) if not e.get("isDeleted")]
    if not elements:
        print("ERROR: No visible elements found.", file=sys.stderr)
        sys.exit(1)

    # Check canvas server
    health = check_server()
    if not health:
        print("ERROR: Canvas server not running.", file=sys.stderr)
        print("  Start it with: cd ~/Dev/mcp_excalidraw && PORT=3000 npm run canvas", file=sys.stderr)
        sys.exit(1)

    ws_clients = health.get("websocket_clients", 0)

    # Auto-open headless browser if needed
    browser = None
    playwright_ctx = None
    if ws_clients == 0:
        if not headless:
            print("ERROR: No browser connected to canvas server.", file=sys.stderr)
            print("  Open http://localhost:3000 in a browser, or use --headless flag.", file=sys.stderr)
            sys.exit(1)
        try:
            from playwright.sync_api import sync_playwright
            playwright_ctx = sync_playwright().__enter__()
            browser = playwright_ctx.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(CANVAS_URL)
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(1)
        except ImportError:
            print("ERROR: Playwright not installed. Install with: pip install playwright && playwright install chromium", file=sys.stderr)
            sys.exit(1)

    try:
        # Clear canvas first, then import
        import urllib.request as _ur
        req = _ur.Request(f"{CANVAS_URL}/api/elements/clear", data=b"", method="DELETE")
        with _ur.urlopen(req, timeout=10):
            pass

        time.sleep(0.5)

        result = post_json("/api/elements/batch", {
            "elements": elements,
            "replaceExisting": False,
        })
        if not result.get("success"):
            print(f"ERROR: Failed to import elements: {result}", file=sys.stderr)
            sys.exit(1)

        time.sleep(1.5)

        # Export as PNG
        export = post_json("/api/export/image", {"format": "png", "background": True})
        if not export.get("success"):
            print(f"ERROR: Export failed: {export}", file=sys.stderr)
            sys.exit(1)

        # Decode and save
        raw = export["data"]
        if "," in raw:
            raw = raw.split(",", 1)[1]
        png_bytes = base64.b64decode(raw)

        if output_path is None:
            output_path = excalidraw_path.with_suffix(".png")

        output_path.write_bytes(png_bytes)
        return output_path

    finally:
        if browser:
            browser.close()
        if playwright_ctx:
            playwright_ctx.__exit__(None, None, None)


def main():
    parser = argparse.ArgumentParser(description="Render .excalidraw to PNG via local canvas server")
    parser.add_argument("input", help="Path to .excalidraw file")
    parser.add_argument("--output", help="Output PNG path (default: same name as input)")
    parser.add_argument("--scale", type=int, default=2, help="Device scale factor (default: 2)")
    parser.add_argument("--headless", action="store_true",
                        help="Auto-open a headless browser if no client is connected")
    args = parser.parse_args()

    excalidraw_path = Path(args.input).resolve()
    if not excalidraw_path.exists():
        print(f"ERROR: File not found: {excalidraw_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output).resolve() if args.output else None
    png_path = render(excalidraw_path, output_path, args.scale, args.headless)
    print(f"PNG saved: {png_path}")


if __name__ == "__main__":
    main()
