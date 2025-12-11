# MD2TeX: Full-Stack Markdown to LaTeX Converter

[English](#md2tex-full-stack-markdown-to-latex-converter) | [中文说明](#md2tex-全栈-markdown-转-latex-转换器)

---

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

---

# MD2TeX 全栈 Markdown 转 LaTeX 转换器

MD2TeX 是一个现代化的全栈 Web 工具，旨在将增强版 Markdown（支持中文、数学公式、表格和交叉引用）转换为高质量的 LaTeX 文档。它拥有基于 React 和 Monaco Editor 的双栏编辑器，以及基于 FastAPI 的高性能渲染后端。

## ✨ 核心特性

- **双栏实时编辑**: 左侧 Markdown 写作，右侧实时预览 LaTeX 代码（使用 VS Code 同款编辑器）。
- **智能转换引擎**:
  - **数学公式**: 完美支持 `$$...$$` 块级公式和 `$e^{ix}$` 行内公式。
  - **智能表格**: 自动计算列宽，生成标准的 LaTeX `tabular` 环境。
  - **图片管理**: 自动生成带标题（Caption）和标签（Label）的 `figure` 环境。
  - **交叉引用**: 自动为标题/图片生成引用标签，支持 `[链接](#id)` 自动转为 `\ref`。
- **多模板切换**: 支持一键切换 **学术论文** 和 **个人简历** 模板。
- **数据持久化**: 自动保存内容到浏览器本地存储，防止丢失。
- **AI 助手**: (演示版) 悬浮式 AI 助手 UI，用于文本润色和补全。
- **精美 UI**: 采用现代化的暗色毛玻璃（Glassmorphism）设计风格。

## 🛠️ 技术栈

- **后端**: Python, FastAPI, Mistune (Markdown 解析), Jinja2 (LaTeX 模板).
- **前端**: React, Vite, Monaco Editor, Axios.
- **设计**: 原生 CSS 变量, 深色主题设计系统.

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+

### 安装步骤

1. **启动后端 (Backend)**
   ```bash
   cd backend
   pip install fastapi uvicorn mistune jinja2
   python -m backend.main
   ```
   后端服务将运行在 `http://localhost:8000`.

2. **启动前端 (Frontend)**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   前端页面将运行在 `http://localhost:5173`.

## 📝 使用指南

1. 打开前端页面 URL。
2. 在左侧输入 Markdown 内容。
3. 右侧即时生成可编译的 LaTeX 代码。
4. 点击右上角的 **Download .tex** 下载文件。
5. 点击顶部的 **设置 (⚙️)** 图标修改作者姓名或调整字号。

## 📄 开源协议

MIT
