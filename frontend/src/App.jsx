import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import Editor from '@monaco-editor/react'

function App() {
    const [mdContent, setMdContent] = useState("# Start typing...\n\nHello World");
    const [texCode, setTexCode] = useState("");
    const [status, setStatus] = useState("Ready");
    const [templateType, setTemplateType] = useState("article");
    const [aiPanelOpen, setAiPanelOpen] = useState(false);
    const [settingsOpen, setSettingsOpen] = useState(false);
    const [config, setConfig] = useState({ author: "Anonymous", fontSize: 14 });
    const [aiInput, setAiInput] = useState("");
    const [aiResult, setAiResult] = useState("");
    const [aiLoading, setAiLoading] = useState(false);
    const editorRef = useRef(null);

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;
    }

    const runAI = async (command) => {
        if (!aiInput && command !== 'polish') return;
        setAiLoading(true);
        try {
            let textToSend = aiInput;
            if (command === 'polish' && !textToSend && editorRef.current) {
                const model = editorRef.current.getModel();
                const selection = editorRef.current.getSelection();
                textToSend = model.getValueInRange(selection);
            }
            if (!textToSend) {
                alert("Please select text or type a command.");
                setAiLoading(false);
                return;
            }
            const response = await axios.post('http://localhost:8000/api/ai_assist', {
                command: command,
                text: textToSend
            });
            setAiResult(response.data.result);
        } catch (error) {
            console.error(error);
            setAiResult("Error calling AI.");
        }
        setAiLoading(false);
    };

    const insertResult = () => {
        if (editorRef.current && aiResult) {
            const editor = editorRef.current;
            const selection = editor.getSelection();
            const op = { range: selection, text: aiResult, forceMoveMarkers: true };
            editor.executeEdits("ai-insert", [op]);
            setMdContent(editor.getValue());
        }
    };

    useEffect(() => {
        const saved = localStorage.getItem('mdContent');
        if (saved) setMdContent(saved);

        try {
            const savedConfig = localStorage.getItem('mdConfig');
            if (savedConfig) {
                const parsed = JSON.parse(savedConfig);
                if (parsed && typeof parsed === 'object') {
                    setConfig(prev => ({ ...prev, ...parsed }));
                }
            }
        } catch (e) {
            console.error("Failed to load config", e);
            localStorage.removeItem('mdConfig');
        }
    }, []);

    useEffect(() => {
        const timer = setTimeout(async () => {
            if (!mdContent) return;
            localStorage.setItem('mdContent', mdContent);
            // Save config too
            localStorage.setItem('mdConfig', JSON.stringify(config));

            setStatus("Converting...");
            try {
                const response = await axios.post('http://localhost:8000/api/convert', {
                    content: mdContent,
                    template_type: templateType,
                    author: config.author // Pass author from settings
                });
                setTexCode(response.data.latex_code);
                setStatus("Done");
            } catch (error) {
                console.error("Conversion error:", error);
                setStatus("Error");
            }
        }, 500);
        return () => clearTimeout(timer);
    }, [mdContent, templateType, config]); // Re-run when config changes

    return (
        <div className="app-container">
            <header className="app-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                    <div className="brand">
                        MD2TeX <span className="brand-subtitle">Full Stack Edition</span>
                    </div>
                    <select
                        className="template-select"
                        value={templateType}
                        onChange={(e) => setTemplateType(e.target.value)}
                    >
                        <option value="article">Article Template</option>
                        <option value="resume">Resume Template</option>
                    </select>
                </div>
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <button
                        className="btn btn-secondary"
                        onClick={() => setSettingsOpen(true)}
                        title="Settings"
                    >
                        ⚙️
                    </button>
                    <button
                        className="btn btn-ai"
                        onClick={() => setAiPanelOpen(!aiPanelOpen)}
                    >
                        ✨ AI Copilot
                    </button>
                    <span style={{ fontSize: '0.85rem', color: status === 'Done' ? '#4caf50' : '#888' }}>
                        {status === 'Converting...' ? '⟳ Syncing...' : status}
                    </span>
                </div>
            </header>

            <div className="main-content">
                {/* Editor Pane */}
                <div className="editor-pane">
                    <div className="pane-header">Markdown Input</div>
                    <Editor
                        height="100%"
                        defaultLanguage="markdown"
                        theme="vs-dark"
                        value={mdContent}
                        onChange={(value) => setMdContent(value)}
                        onMount={handleEditorDidMount}
                        options={{
                            minimap: { enabled: false },
                            fontSize: config.fontSize,
                            wordWrap: 'on',
                            padding: { top: 16, bottom: 16 },
                            fontFamily: "'Fira Code', Consolas, Monaco, monospace",
                        }}
                    />
                </div>

                {/* Preview Pane */}
                <div className="preview-pane">
                    <div className="pane-header">
                        <span>LaTeX Output</span>
                        <button
                            className="btn btn-download"
                            onClick={() => {
                                const blob = new Blob([texCode], { type: 'text/plain' });
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'document.tex';
                                a.click();
                                URL.revokeObjectURL(url);
                            }}
                            style={{ fontSize: '0.8rem', padding: '2px 8px' }}
                        >
                            Download .tex
                        </button>
                    </div>
                    <Editor
                        height="100%"
                        defaultLanguage="latex"
                        theme="vs-dark"
                        value={texCode}
                        options={{
                            readOnly: true,
                            minimap: { enabled: false },
                            fontSize: config.fontSize,
                            wordWrap: 'on',
                            padding: { top: 16, bottom: 16 },
                            fontFamily: "'Fira Code', Consolas, monospace",
                            backgroundColor: '#1e1e1e'
                        }}
                    />
                    <div className="hints-bar" style={{ overflowX: 'auto', whiteSpace: 'nowrap' }}>
                        <strong>💡 Quick Tips:</strong>
                        <span style={{ marginLeft: '15px' }}><code>&gt; 定理 (名)</code> Theorem Box</span>
                        <span style={{ marginLeft: '15px' }}><code>&gt; 问题</code> Question Box</span>
                        <span style={{ marginLeft: '15px' }}><code>$$...$$</code> Block Math</span>
                        <span style={{ marginLeft: '15px' }}><code>{'$e^{ix}$'}</code> Inline Math</span>
                        <span style={{ marginLeft: '15px' }}><code>[Link](#h1)</code> Auto-Ref</span>
                        <span style={{ marginLeft: '15px' }}><code>![Alt](src)</code> Figure</span>
                        <span style={{ marginLeft: '15px' }}><code>| A | B |</code> Table</span>
                    </div>
                </div>
            </div>

            {/* AI Panel */}
            {aiPanelOpen && (
                <div className="ai-panel">
                    <div className="ai-header">
                        <span>🤖</span> AI Assistant
                        <button onClick={() => setAiPanelOpen(false)} style={{ marginLeft: 'auto', background: 'none', border: 'none', color: '#ccc', cursor: 'pointer' }}>×</button>
                    </div>
                    <div className="ai-body">
                        <textarea
                            className="ai-input"
                            value={aiInput}
                            onChange={(e) => setAiInput(e.target.value)}
                            placeholder="Instruction or select text..."
                        />
                        <div className="ai-controls">
                            <button className="btn btn-primary btn-ai" style={{ flex: 1, justifyContent: 'center' }} onClick={() => runAI('polish')} disabled={aiLoading}>
                                {aiLoading ? '...' : '💅 Polish'}
                            </button>
                            <button className="btn btn-secondary" onClick={() => runAI('complete')} disabled={aiLoading}>
                                ✍️
                            </button>
                        </div>
                        {aiResult && (
                            <div className="ai-result">
                                {aiResult}
                                <button className="btn btn-download"
                                    style={{ width: '100%', marginTop: '8px', padding: '4px', justifyContent: 'center' }}
                                    onClick={insertResult}
                                >
                                    Insert
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Settings Modal */}
            {settingsOpen && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    backgroundColor: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)',
                    display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 200
                }}>
                    <div style={{
                        width: '400px', background: '#1e1e1e', border: '1px solid #3e3e3e',
                        borderRadius: '12px', padding: '24px', boxShadow: '0 10px 40px rgba(0,0,0,0.5)'
                    }}>
                        <h2 style={{ marginTop: 0, fontSize: '1.4rem' }}>Settings</h2>

                        <div style={{ marginBottom: '16px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', color: '#ccc' }}>Author Name (for LaTeX)</label>
                            <input
                                type="text"
                                value={config.author}
                                onChange={(e) => setConfig({ ...config, author: e.target.value })}
                                style={{ width: '100%', padding: '8px', background: '#2d2d2d', border: '1px solid #3e3e3e', color: 'white', borderRadius: '4px' }}
                            />
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', color: '#ccc' }}>Editor Font Size ({config.fontSize}px)</label>
                            <input
                                type="range"
                                min="10" max="24"
                                value={config.fontSize}
                                onChange={(e) => setConfig({ ...config, fontSize: parseInt(e.target.value) })}
                                style={{ width: '100%' }}
                            />
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                            <button
                                className="btn btn-download"
                                onClick={() => setSettingsOpen(false)}
                            >
                                Close & Save
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default App
