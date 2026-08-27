from playwright.sync_api import sync_playwright

print("Step 1: Opening Chrome browser...")

with sync_playwright() as p:

    # Open installed Google Chrome
    browser = p.chromium.launch(
        channel="chrome",
        headless=False
    )

    page = browser.new_page()

    print("Step 2: Launching Cricbuzz website...")

    page.goto("https://www.cricbuzz.com/", wait_until="domcontentloaded")

    # Wait for the page to load
    page.wait_for_timeout(5000)

    print("Step 3: Fetching live cricket scores...")

    # Get all visible text from the webpage
#    cricket_scores = page.locator("body").inner_text()

#   print("\n========== CRICBUZZ LIVE SCORES ==========\n")
#   print(cricket_scores)
#   print("\n===========================================\n")

#   input("Press Enter to close Chrome...")

 # Find the live matches section
    live_section = page.locator(
       "main.min-h-container div.carousal-list" # "div.cb-col.cb-col-100.cb-lv-main"
    )

    # Find individual match cards
    match_cards = live_section.locator(
        "div.carousal-item" #"div.cb-mtch-lst"
    )

    count = match_cards.count()

    print(f"\nNumber of live/recent match cards found: {count}\n")

    print("=" * 70)
    print("              CRICBUZZ LIVE SCORES")
    print("=" * 70)

    if count == 0:
        print("No live matches found.")
    else:

        for i in range(count):

            card = match_cards.nth(i)

            # Get text from individual card
            text = card.inner_text().strip()

            if text:
                print(f"\nMATCH {i + 1}")
                print("-" * 70)
                print(text)

    print("\n" + "=" * 70)

    input("\nPress Enter to close Chrome...")

    browser.close()

print("Browser closed.")