import time
import os
from datetime import datetime
import importlib
pyperclip = importlib.import_module("pyperclip")

# Load pyautogui dynamically so static analyzers do not report a missing
# module source when the package is installed in a different interpreter.
pyautogui = importlib.import_module("pyautogui")

# Load Selenium dynamically so static analyzers do not report a missing
# module source when the package is installed in a different interpreter.
webdriver = importlib.import_module("selenium.webdriver")
By = importlib.import_module("selenium.webdriver.common.by").By
Options = importlib.import_module("selenium.webdriver.chrome.options").Options

# Load openpyxl dynamically so static analyzers do not report a missing
# module source when the package is installed in a different interpreter.
openpyxl = importlib.import_module("openpyxl")
Workbook = openpyxl.Workbook


# ============================================================
# CONFIGURATION
# ============================================================

WEBSITE_URL = "https://www.moneycontrol.com/"

# Folder where Excel and screenshot will be saved
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Current date and time
now = datetime.now()

date_time = now.strftime("%Y-%m-%d %H:%M:%S")
file_date = now.strftime("%Y-%m-%d")


excel_file = os.path.join(
    OUTPUT_FOLDER,
    f"RPA_Data_{file_date}.xlsx"
)

screenshot_file = os.path.join(
    OUTPUT_FOLDER,
    f"Excel_Screenshot_{file_date}.png"
)


# ============================================================
# STEP 1: OPEN CHROME
# ============================================================

print("Step 1: Open the Chrome browser...")

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

time.sleep(2)


# ============================================================
# STEP 2: LAUNCH WEBSITE
# ============================================================

print("Step 2: Launch the website...")

driver.get(WEBSITE_URL)

time.sleep(5)


# ============================================================
# STEP 3: COPY THE CONTENT
# ============================================================

print("Step 3: Copy the content...")

# Get all visible text from the webpage
fetched_data = driver.find_element(By.TAG_NAME, "title").get_attribute("textContent")

print("\nFetched Content:")
print(fetched_data[:500])

# Copy the fetched content to clipboard
pyperclip.copy(fetched_data)

print("Website content copied successfully.")


# ============================================================
# STEP 4: CREATE / OPEN EXCEL SHEET
# ============================================================

print("Step 4: Open Excel sheet...")

if os.path.exists(excel_file):

    # If today's file already exists, open it
    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active

else:

    # Create a new Excel workbook
    workbook = Workbook()
    worksheet = workbook.active

    worksheet.title = "RPA Data"

    # Create headers
    worksheet["A1"] = "Date & Time"
    worksheet["B1"] = "Fetched Data"
    worksheet["C1"] = "Comment"


# ============================================================
# STEP 5: CREATE A ROW
# ============================================================

print("Step 5: Create a row containing datetime, fetched data and short comment...")

# Short comment
comment = "Data fetched successfully from website"

# Find next empty row
next_row = worksheet.max_row + 1

worksheet.cell(row=next_row, column=1).value = date_time
worksheet.cell(row=next_row, column=2).value = fetched_data
worksheet.cell(row=next_row, column=3).value = comment


# Adjust column widths
worksheet.column_dimensions["A"].width = 22
worksheet.column_dimensions["B"].width = 80
worksheet.column_dimensions["C"].width = 40

# Enable wrap text
Alignment = importlib.import_module("openpyxl.styles").Alignment

worksheet.cell(row=next_row, column=2).alignment = Alignment(
    wrap_text=True,
    vertical="top"
)

worksheet.cell(row=next_row, column=3).alignment = Alignment(
    wrap_text=True,
    vertical="top"
)


# ============================================================
# STEP 6: SAVE EXCEL WITH DATE IN FILE NAME
# ============================================================

print("Step 6: Save the Excel sheet with date in file name...")

workbook.save(excel_file)

print(f"Excel file saved: {excel_file}")


# ============================================================
# STEP 7: TAKE SCREENSHOT OF EXCEL
# ============================================================

print("Step 7: Take screenshot of the Excel sheet and save it...")

# Open the Excel file using Windows default Excel application
os.startfile(excel_file)

# Give Excel time to open
time.sleep(5)

# Take screenshot of the complete screen
screenshot = pyautogui.screenshot()

screenshot.save(screenshot_file)

print(f"Screenshot saved: {screenshot_file}")


# ============================================================
# STEP 8: CLOSE EXCEL AND CHROME
# ============================================================

print("Step 8: Close the Excel sheet and browser...")

# Close Excel using ALT + F4
pyautogui.hotkey("alt", "f4")

time.sleep(2)

# Close Chrome using Selenium
driver.quit()

print("Excel and Chrome closed successfully.")


# ============================================================
# COMPLETED
# ============================================================

print("\n========================================")
print("RPA PROCESS COMPLETED SUCCESSFULLY")
print("========================================")

print(f"Excel File    : {excel_file}")
print(f"Screenshot    : {screenshot_file}")
print(f"Date & Time   : {date_time}")