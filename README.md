☕ Café NovaBot - AI-Powered Café Chatbot Ordering System

Café NovaBot is an intelligent, interactive chatbot built using Python and Flask that allows users to place café orders through a conversational interface. Designed for cafés and small food businesses, NovaBot provides a seamless ordering experience with a visually appealing UI and a smart chatbot that handles everything from order intake to confirmation and digital receipt generation.

---

🚀 Features

- 🗨️ Chatbot-based ordering interface
- 📋 Real-time menu display with prices and images
- ✅ Add, confirm, or cancel orders using simple messages
- 🧾 Generates a detailed receipt with GST (5%) calculation
- 💾 Stores confirmed orders in a JSON file (no database required)
- 🎨 Clean, responsive UI with menu images and chatbot popup
- 🔒 Session-based order handling

---

 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Backend:** Python, Flask
- **Data Storage:** JSON files (`menu.json`, `orders.json`)
- **Session Handling:** Flask `session`

---
***** move images folder to static folder or else reroute the images in code****

## 📂 Project Structure
cafe_chatbot_project/
│
├── app.py # Flask backend logic
├── data/
│ ├── menu.json # Menu items with names, prices, and images
│ └── orders.json # Stores confirmed orders
├── templates/
│ ├── home.html # Homepage UI
│ ├── chat.html # Chatbot and menu interface
│ └── order_confirmed.html # Receipt display page
├── static/
│ ├── style.css # Styling for pages
│ └── images/ # Menu and chatbot icon images
└── README.md # You're reading it!
