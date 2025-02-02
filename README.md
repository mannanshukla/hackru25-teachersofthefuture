# 💋 AI-Powered Beamer Presentation Generator

This is a **full-stack web application** that generates **Beamer LaTeX presentations** using **TailwindCSS, FastAPI, and the Ollama API**. The app allows users to enter a **topic, notes, and a reading level**, then compiles a **Beamer PDF** which is displayed in the browser.

---

## **🚀 Features**
✔ **User-friendly web form** for inputting presentation details  
✔ **Ollama AI** generates structured and readable Beamer LaTeX code  
✔ **Automatic LaTeX PDF compilation** using `pdflatex`  
✔ **Embedded PDF viewer** for viewing generated presentations  
✔ **Logging for debugging issues**  

---

## **📌 Setup Guide (Run Locally)**

Follow these steps to install and run everything **from scratch** on your local machine.

### **1️⃣ Install Dependencies**
Ensure you have the following installed:
- **Python 3.11+**
- **Node.js & npm**
- **Ollama AI (`llama3.2` model)**
- **LaTeX (`pdflatex`)**
- **FastAPI & Uvicorn**

#### **🛠️ Install Homebrew (Mac)**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### **🛠️ Install Python & Node.js**
```bash
brew install python@3.11 node
```

#### **🛠️ Install LaTeX (`pdflatex`)**
```bash
brew install mactex
```
_(For Linux, use: `sudo apt install texlive-full`)_

---

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### **3️⃣ Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

---

### **4️⃣ Install Python Dependencies**
```bash
pip install -r requirements.txt
```

---

### **5️⃣ Install and Set Up TailwindCSS**
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

### **6️⃣ Start Ollama API**
Ensure **Ollama** is running before starting the FastAPI server.

```bash
ollama serve
```

Check if it's working:
```bash
curl http://127.0.0.1:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Test connection",
  "stream": false
}'
```
Expected Output: `"response": "Some AI-generated text..."`

---

### **7️⃣ Start FastAPI Backend**
```bash
uvicorn backend.main:app --reload
```

---

### **8️⃣ Run the Frontend**
```bash
cd frontend
npm install
npm run dev
```
The **frontend will now be running on** `http://localhost:3000`.

---

### **9️⃣ Generate a Presentation**
Send a **POST request** to generate a Beamer LaTeX presentation.

```bash
curl -X POST http://127.0.0.1:8000/generate_presentation/ -H "Content-Type: application/json" -d '{
  "topic": "Climate Change",
  "notes": "Effects on weather, economy, and human health",
  "reading_level": "10th Grade"
}'
```
This should return:
```json
{
  "pdf_url": "/pdf_output/presentation.pdf"
}
```

---

### **🔟 View the Embedded Presentation**
Open in your browser:
```
http://127.0.0.1:8000/embed_presentation/
```
This will **embed the generated PDF in an HTML page**.

---

## **🛠️ Troubleshooting**
### **🚨 PDF Not Embedding?**
- Ensure **pdflatex is installed** and working:
  ```bash
  pdflatex --version
  ```
- Check if **output directory exists**:
  ```bash
  ls output
  ```

### **🚨 Ollama API Failing?**
- Make sure **Ollama is running** before starting the backend:
  ```bash
  ollama serve
  ```

### **🚨 FastAPI Not Starting?**
- Ensure your virtual environment is activated:
  ```bash
  source venv/bin/activate
  ```

---

## **💚 Directory Structure**
```
/your-repo
│── backend/
│   ├── main.py  # FastAPI Backend
│   ├── requirements.txt
│   ├── logs/  # Error logs
│   ├── output/  # Generated PDFs
│── frontend/
│   ├── index.html  # UI Form
│   ├── output.css  # Tailwind Styles
│   ├── app.js  # JavaScript Logic
│── README.md
```

---

## **🌟 Next Steps**
- ✅ **Test**: Ensure presentation generation works smoothly  
- 💤 **Improve AI Prompting**: Fine-tune LaTeX structure for cleaner slides  
- 🎨 **Enhance UI**: Make frontend more interactive  

---

### 🚀 **You're all set! Now start generating Beamer slides with AI!**
```
uvicorn backend.main:app --reload
npm run dev
```
🔥 **Built for HackRU 2025 – AI for Educators!**

## Tracks:
- GenAI
- Reach Capital future of work + education track with AI
- Best Use of Terraform
- Best GoDaddy domain
- Social Good + Education Track for HackRU
