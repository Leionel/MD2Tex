# MD2TeX: Full-Stack Markdown to LaTeX Converter

MD2TeX is a modern, web-based tool designed to convert enhanced Markdown (including Chinese, Math, Tables, and Cross-references) into high-quality LaTeX documents. It features a React frontend with a Monaco Editor and a FastAPI backend with a custom-engineered rendering engine.

## ✨ Features

- **Dual-Pane Editor**: Real-time writing and LaTeX preview using Monaco Editor.
- **Smart Conversion**:
  - **Math**: Supports `$$...$$` and `$e^{ix}$` with LaTeX-safe rendering.
  - **Tables**: Auto-calculates column widths for robust `tabular` environments.
  - **Images**: Auto-generates `figure` environments with captions and labels.
  - **Cross-refs**: Auto-generates `\label` for headers/images and supports `[Link](#id)` -> `\ref`.
- **Templates**: Switch between `Article` and `Resume` templates instantly.
- **Data Persistence**: Auto-saves your work to LocalStorage.
- **AI Copilot**: (Mock) UI for AI-assisted text polishing and completion.
- **Premium UI**: Dark mode glassmorphism design.

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, Mistune (Markdown Parser), Jinja2 (Templating).
- **Frontend**: React, Vite, Monaco Editor, Axios.
- **Styling**: CSS Variables, Dark Theme.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+

### Installation

1. **Backend Setup**
   ```bash
   cd backend
   pip install fastapi uvicorn mistune jinja2
   python -m backend.main
   ```
   Server runs at `http://localhost:8000`.

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Client runs at `http://localhost:5173`.

## 📝 Usage

1. Open the frontend URL.
2. Type Markdown in the left pane.
3. See formatted LaTeX code in the right pane.
4. Click **Download .tex** to save the file.
5. Use **Settings** (⚙️) to change Author Name or Font Size.

## 📄 License

MIT
