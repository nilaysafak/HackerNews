from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import ttk
import webbrowser

def open_url(url):
    webbrowser.open_new(url)

def fetch_news():
    url = 'https://news.ycombinator.com'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_items = []
    for item in soup.find_all('tr', class_='athing'):
        title_span = item.find('span', class_='titleline')
        if title_span:
            title = title_span.a.text
            link = title_span.a['href']
            if not link.startswith('http'):
                link = f"https://news.ycombinator.com/{link}"
            if not title.startswith('Show HN:') and 'Serena' not in title:
                news_items.append((title, link))
    
    return news_items

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Hacker News")
root.geometry("800x600+400+100")  # Pencereyi sağa kaydır
root.configure(bg='#f0f0f0')  # Arka plan rengi

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 10), borderwidth=1, relief="flat", background="#808080", foreground="white")  # Gri renk
style.map('TButton', background=[('active', '#696969')])  # Koyu gri (hover efekti için)

# Frame oluştur
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Canvas ve scrollbar
canvas = tk.Canvas(main_frame, bg='#f0f0f0')
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# "News" etiketini ekle
news_label = ttk.Label(scrollable_frame, text="Hacker News", font=("Arial", 24, "bold"), background='#f0f0f0', foreground='#333333')
news_label.pack(pady=20)

# Haberleri getir ve butonları oluştur
news_items = fetch_news()
for i, (title, url) in enumerate(news_items):
    button = ttk.Button(scrollable_frame, text=title, command=lambda u=url: open_url(u))
    button.pack(pady=5, padx=50, fill=tk.X)
    
    # Her 2 butondan sonra ayırıcı ekle
    if i % 2 == 1:
        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=tk.X, padx=50, pady=10)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()