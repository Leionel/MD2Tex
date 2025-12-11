from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mistune
from jinja2 import Environment, FileSystemLoader
from backend.models import ConvertRequest, ConvertResponse, AIRequest, AIResponse
from backend.renderer import LaTeXRenderer

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/ai_assist", response_model=AIResponse)
async def ai_assist(request: AIRequest):
    # TODO: Integrate with Real LLM (OpenAI/Anthropic)
    # For now, we return a mock response to demonstrate UI flow
    
    result = ""
    if request.command == "polish":
        result = f"Better version: {request.text} (Polished by AI)"
    elif request.command == "complete":
        result = f"{request.text} ... [AI Completed Text]"
    else:
        result = f"I heard: {request.text}"
        
    return AIResponse(result=result, status="success")

@app.post("/api/convert", response_model=ConvertResponse)
async def convert_markdown(request: ConvertRequest):
    # Initialize renderer
    renderer = LaTeXRenderer()
    
    try:
        # Import plugins explicitly
        import mistune
        from mistune.plugins.table import table as table_plugin
        
        # We disable math plugin because we handle it manually in renderer
        markdown = mistune.create_markdown(
            renderer=renderer, 
            plugins=[table_plugin] 
        )
        
        # Convert content
        latex_body = markdown(request.content)
        
        # Load Jinja2 template
        # Use absolute path to be sure
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, "templates")
        print(f"DEBUG: Template Dir: {template_dir}")
        
        env = Environment(
            loader=FileSystemLoader(template_dir),
            block_start_string='\\BLOCK{',
            block_end_string='}',
            variable_start_string='\\VAR{',
            variable_end_string='}',
            comment_start_string='\\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
        )
        template = env.get_template(f"{request.template_type}.tex")
        
        # Render full LaTeX
        latex_full = template.render(
            title="Converted Document", # We could let user specify this
            author=request.author,
            body=latex_body
        )

        return ConvertResponse(
            latex_code=latex_full,
            status="success"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return ConvertResponse(
            latex_code=f"ERROR: {str(e)}\n{traceback.format_exc()}",
            status="error"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
