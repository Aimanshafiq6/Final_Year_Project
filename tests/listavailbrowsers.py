import webbrowser

def get_available_browsers():
    browsers = [
        'Firefox',
        'Chrome',
        'Safari',
        'Opera',
        'Edge',
        'Internet-explorer',
        'Brave',
        'Chromium',
    ]

    available_browsers = []

    for browser in browsers:
        try:
            b = webbrowser.get(browser)
            available_browsers.append(browser)
            print(b.basename)
        except webbrowser.Error:
            pass

    return available_browsers

# Get and print the list of available browsers
available = get_available_browsers()
print("Available browsers:")
for browser in available:
    print(f"- {browser}")

# Get the default browser
default_browser = webbrowser.get().name
print(f"\nDefault browser: {default_browser}")