from playwright.sync_api import sync_playwright
import time
import random
from config import STATE_FILE
from llm_helper import generate_response

# --- CONFIGURATION ---
# Set to True to ONLY type the message but NOT send it.
# Set to False to actually send messages.
DRAFT_MODE = True 

# Keywords to trigger the response
KEYWORDS = [
    "developer", "vývojář", "programátor",
    "marketing", "seo", "ppc",
    "gtm", "go to market",
    "ai process", "ai agent", "ai řešení",
    "outsourcing", "nearshoring", "staff augmentation",
    "full stack", "backend", "frontend",
    "sales", "lead gen", "akvizice",
    "recruitment", "recruiting", "hiring", "nábor",
    "external team", "dedicated team", "software development"
]

def run_bot():
    print(f"Starting LinkedIn Bot... (DRAFT_MODE={DRAFT_MODE})")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=STATE_FILE)
        page = context.new_page()
        
        print("Navigating to Messaging...")
        page.goto("https://www.linkedin.com/messaging/")
        
        # Wait for messages to load
        try:
            page.wait_for_selector(".msg-conversation-listitem", timeout=15000)
        except:
            print("Could not find conversation list. Are you logged in?")
            return

        # Scroll to load more conversations
        print("Scrolling to load more conversations...")
        conversation_list_selector = ".msg-conversations-container__conversations-list" # Common container class
        # Fallback if container class changed: just scroll the sidebar area
        
        for _ in range(5): # Scroll 5 times
            # Try to find the last conversation item and scroll it into view
            convs = page.query_selector_all(".msg-conversation-listitem")
            if convs:
                convs[-1].scroll_into_view_if_needed()
            time.sleep(1.5) # Wait for lazy load

        # Get list of conversations (limit to 50)
        conversations = page.query_selector_all(".msg-conversation-listitem")[:50]
        print(f"Found {len(conversations)} conversations to check.")
        
        for i, conv in enumerate(conversations):
            try:
                # Click conversation
                conv.click()
                # Random delay to look human
                time.sleep(random.uniform(1.5, 3))
                
                # 1. Check if we already replied (Safety Check)
                # We look at the conversation history bubbles
                message_items = page.query_selector_all(".msg-s-event-listitem")
                if not message_items:
                    continue
                
                # Check the last few messages for our signature
                already_replied = False
                for item in message_items[-3:]: # Check last 3 messages
                    bubble = item.query_selector(".msg-s-event-listitem__body")
                    if bubble:
                        text = bubble.inner_text()
                        if "Automatic robot" in text or "automatický robot" in text:
                            already_replied = True
                            break
                
                if already_replied:
                    print(f"[{i}] Skipping: We already replied.")
                    continue

                # 2. Get the last message to analyze
                last_bubble = message_items[-1].query_selector(".msg-s-event-listitem__body")
                if not last_bubble:
                    continue
                
                last_message = last_bubble.inner_text()
                
                # Get sender name for logging
                sender_name_el = page.query_selector(".msg-entity-lockup__entity-title")
                sender_name = sender_name_el.inner_text() if sender_name_el else "Unknown"
                
                print(f"[{i}] Checking conversation with {sender_name}...")
                
                # 3. Keyword Matching
                found_keyword = next((k for k in KEYWORDS if k in last_message.lower()), None)
                
                if found_keyword:
                    print(f"    -> MATCH! Keyword: '{found_keyword}'")
                    
                    # 4. Generate Response
                    print("    -> Generating response...")
                    response_text = generate_response(last_message, sender_name)
                    
                    if response_text:
                        print(f"    -> Response ready ({len(response_text)} chars).")
                        
                        # 5. Type into the box
                        msg_box = page.query_selector(".msg-form__contenteditable")
                        if msg_box:
                            print("    -> Typing response...")
                            msg_box.fill(response_text)
                            
                            if DRAFT_MODE:
                                print("    -> DRAFT MODE: Message typed.")
                                print("    -> ACTION REQUIRED: Review the message in the browser.")
                                print("       - If you like it, click SEND manually.")
                                print("       - If not, edit or delete it.")
                                input("    -> Press Enter in this terminal when ready to move to the next conversation...")
                            else:
                                print("    -> SENDING...")
                                time.sleep(1)
                                page.keyboard.press("Enter")
                                print("    -> SENT!")
                                time.sleep(1)
                        else:
                            print("    -> ERROR: Could not find message input box.")
                    else:
                        print("    -> ERROR: LLM failed to generate response.")
                else:
                    print("    -> No keywords found.")
                    
            except Exception as e:
                print(f"Error processing conversation {i}: {e}")
        
        print("\nDone checking conversations.")
        if DRAFT_MODE:
            print("Draft mode finished. You can inspect the browser window.")
            input("Press Enter in the terminal to close the browser...")
        
        browser.close()

if __name__ == "__main__":
    run_bot()
