# 📌 Bookmark-AI-Organizer

🚀 **Bookmark-AI-Organizer** is a CLI tool designed to export bookmarks from your browser, process them using OpenAI to enhance metadata (title, description, seniority level, tags, URL), and store them in Notion.

---

## 🌟 Features
✅ Export bookmarks from your browser (all or specific folders).  
✅ Process bookmarks with OpenAI to enrich metadata.  
✅ Automatically save structured data to Notion.  
✅ Supports automatic dependency installation.  
✅ Uses a `.cache` file to track processed bookmarks, avoiding duplicates in Notion.  

---

## 🛠️ Tech Stack
- **OpenAI API** 🧠
- **Notion API** 📖
- **Asyncio & Aiohttp** ⚡
- **Pydantic** ✅

---

## 💾 Requirements
- **Python 3.8+** 🐍
- **Supported OS:** Windows, Linux, macOS (Darwin) 🖥️
- **OpenAI & Notion API accounts** 🔑

---

## 🔧 Installation & Setup
### 1️⃣ Clone the repository:
```bash
git clone https://github.com/user/Bookmark-AI-Organizer.git
cd Bookmark-AI-Organizer
```

### 2️⃣ Set up environment variables:
Create a `.env` file and add the required credentials:
```env
OPENAI_API_KEY=your_openai_api_key
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id
```

🔹 **How to get these values?**
- **OpenAI API Key:** [Get it here](https://platform.openai.com/signup/)
- **Notion API Key:** [Create an integration](https://www.notion.so/my-integrations)
- **Notion Database ID:** Open your Notion database, copy the URL, and extract the ID (between `https://www.notion.so/` and `?v=`).

- *[Example Notion Tutorial: ](https://www.pynotion.com/getting-started-with-python/)
---

## ▶️ Running the Application
Run the application in your terminal:
```bash
python main.py [options]
```

### Available Options:
| Parameter    | Description                                   | Default Value    |
|-------------|-----------------------------------------------|------------------|
| `--browser` | Select a browser (`chrome`, `edge`, `brave`). | `chrome`         |
| `--folder`  | Filter bookmarks by folder name.              | -                |
| `--install` | Whether to install required packages.         | `True` |

🔹 **Example Usage:**
```bash
python main.py --browser brave --folder "Programming"
```

---

## 🌍 Supported Browsers
✅ Google Chrome  
✅ Microsoft Edge  
✅ Brave  

## 🖥️ Supported Operating Systems
✅ Windows  
✅ Linux  
✅ macOS (Darwin)  

---

