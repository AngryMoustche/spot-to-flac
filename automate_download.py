from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up paths
input_file = '/home/user/venv/Spotify Library.txt'  # Absolute path to the file containing song names
download_site = 'https://dab.yeet.su/'  # Your downloader website
log_file = 'download_errors.log'  # Log file to store failed downloads

# Set up Firefox browser
driver = webdriver.Firefox()  # Use webdriver.Chrome() for Chrome if needed
driver.get(download_site)
time.sleep(3)  # Wait for the page to load

# Read songs from the Spotify library file
with open(input_file, 'r', encoding='utf-8') as f:
    songs = [line.strip() for line in f if line.strip()]

# Open the log file for writing (append mode)
with open(log_file, 'a', encoding='utf-8') as log:
    for song in songs:
        try:
            print(f"Searching: {song}")

            # Wait for the search box to be available
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for songs, artists, or albums..."]'))  # XPath with placeholder
            )
            
            # Clear the search box and enter the song name
            search_box.clear()
            search_box.send_keys(song)
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)  # Wait for results to load

            # Locate the song grid container
            song_grid = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'grid'))  # Wait for the grid to be present
            )

            # Find the first song item within the grid
            first_song_item = song_grid.find_element(By.XPATH, './/div[contains(@class, "flex")]')  # Adjust XPath to target the individual song items
            
            # Now find the download button within this first song item
            download_button = first_song_item.find_element(By.XPATH, './/button[contains(@aria-label, "Download track") or contains(text(), "Download FLAC")]')  # XPath
            
            # Click the download button
            download_button.click()
            print(f"Started download for: {song}")
            time.sleep(5)  # Wait for download to start

        except Exception as e:
            # If an error occurs, log it to the file
            log.write(f"Failed to download '{song}': {str(e)}\n")
            print(f"Failed to download '{song}': {e}")
            continue

driver.quit()

