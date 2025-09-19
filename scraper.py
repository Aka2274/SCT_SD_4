import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog

# Function to scrape products
def scrape_products(url, output_file):
    products = []
    response = requests.get(url)
    if response.status_code != 200:
        messagebox.showerror("Error", "Failed to fetch the website!")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract product info (BooksToScrape structure)
    items = soup.find_all('article', class_='product_pod')
    for item in items:
        name = item.h3.a['title']
        price = item.find('p', class_='price_color').text.strip()
        rating = item.p['class'][1]  # Example: "One", "Two", etc.
        products.append([name, price, rating])

    # Save to CSV
    df = pd.DataFrame(products, columns=["Name", "Price", "Rating"])
    df.to_csv(output_file, index=False)
    messagebox.showinfo("Success", f"Data saved to {output_file}")

# GUI Application
def run_gui():
    def start_scraping():
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".csv",
                                                   filetypes=[("CSV Files", "*.csv")])
        if output_file:
            scrape_products(url, output_file)

    root = tk.Tk()
    root.title("E-commerce Scraper")

    tk.Label(root, text="Enter Website URL:").pack(pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=5)

    scrape_button = tk.Button(root, text="Scrape & Save", command=start_scraping)
    scrape_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
