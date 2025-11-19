from playwright.sync_api import sync_playwright
import time
from config import STATE_FILE

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print("Navigating to LinkedIn...")
        page.goto("https://www.linkedin.com/login")
        
        print("Please log in manually in the browser window.")
        print("Waiting for you to reach the feed page (linkedin.com/feed)...")
        
        # Wait for the user to log in and reach the feed
        try:
            page.wait_for_url("**/feed/**", timeout=300000) # 5 minutes timeout
            print("Login detected!")
            
            # Save state
            context.storage_state(path=STATE_FILE)
            print(f"Session saved to {STATE_FILE}")
            
        except Exception as e:
            print(f"Timeout or error: {e}")
        
        browser.close()

if __name__ == "__main__":
    login()
