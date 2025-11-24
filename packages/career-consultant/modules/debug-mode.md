---
module_name: debug-mode
version: 1.0.0
token_cost: ~1500
---

# 🐞 Debug Mode (Developer Console)

This module provides introspection and testing tools for the skill developer. It allows you to inspect prompts, test tools in isolation, and view the current session state.

## When to Load This Module

Load this module when the user explicitly requests debug mode (e.g., `/debug on`, "enable debug mode") or uses a debug command (`/debug prompt`, `/debug tool`).

## Capabilities

1.  **Prompt Inspector**: View the exact system prompts used for specific tasks.
2.  **Tool Tester**: Run MCP tools in isolation with raw output.
3.  **State Viewer**: Dump current session state (loaded modules, token usage, config).
4.  **Verbose Logging**: Toggle detailed execution logs.

## Workflow Steps

### 1. Command Router

Parse the user's debug command and route to the appropriate handler.

```python
def handle_debug_command(command: str, context: dict):
    """
    Route debug commands to handlers.
    
    Args:
        command: The full debug command (e.g., "/debug prompt scoring")
        context: Current session context (config, loaded_modules, etc.)
    """
    parts = command.strip().split()
    if len(parts) < 2:
        return show_debug_help()
        
    action = parts[1].lower()
    args = parts[2:]
    
    if action == "on":
        return enable_debug_mode()
    elif action == "off":
        return disable_debug_mode()
    elif action == "prompt":
        return show_prompt(args[0] if args else None)
    elif action == "tool":
        return test_tool(args[0] if args else None, args[1:] if len(args) > 1 else [])
    elif action == "state":
        return show_state(context)
    elif action == "help":
        return show_debug_help()
    else:
        return f"❌ Unknown debug command: {action}. Type `/debug help` for options."
```

### 2. Prompt Inspector

Display the raw system prompts for specific modules to verify instructions.

```python
def show_prompt(module_name: str):
    """
    Show the system prompt for a specific module.
    """
    prompts = {
        "scoring": "Calculate 6-component score based on...",
        "research": "Research company using Firecrawl/Bright Data...",
        "matching": "Compare CV skills against job requirements...",
        "backlog": "Extract job details and save to YAML..."
    }
    
    if not module_name:
        return "⚠️ Please specify a module: `/debug prompt [scoring|research|matching|backlog]`"
        
    prompt = prompts.get(module_name)
    if prompt:
        return f"""
### 📝 System Prompt: {module_name}

```markdown
{prompt}
```
"""
    else:
        return f"❌ Unknown module: {module_name}. Available: {', '.join(prompts.keys())}"
```

### 3. Tool Tester

Run an MCP tool directly and show the raw output (bypassing normal error handling/formatting).

```python
def test_tool(tool_name: str, args: list):
    """
    Run an MCP tool in isolation.
    """
    if not tool_name:
        return "⚠️ Please specify a tool: `/debug tool [firecrawl|bright_data|filesystem] [args]`"
        
    target = args[0] if args else ""
    
    print(f"🧪 Testing tool: {tool_name} on {target}...")
    
    try:
        if tool_name == "firecrawl":
            # Simulate Firecrawl call
            # result = firecrawl:scrape(url=target)
            result = f"[Mock] Scraped content from {target}..."
            
        elif tool_name == "bright_data":
            # Simulate Bright Data call
            # result = bright_data:scrape_linkedin(url=target)
            result = f"[Mock] LinkedIn profile data for {target}..."
            
        elif tool_name == "filesystem":
            # Simulate Filesystem call
            # result = filesystem:list_directory(path=target)
            result = f"[Mock] Directory listing for {target}..."
            
        else:
            return f"❌ Unknown tool: {tool_name}"
            
        return f"""
### 🧪 Tool Test Result: {tool_name}

**Target**: `{target}`

**Raw Output**:
```json
{result}
```
"""
    except Exception as e:
        return f"❌ Tool Execution Failed:\n```\n{str(e)}\n```"
```

### 4. State Viewer

Dump the current session state for debugging.

```python
def show_state(context: dict):
    """
    Show current session state.
    """
    import json
    
    # Mask sensitive data
    safe_context = context.copy()
    if 'api_keys' in safe_context:
        safe_context['api_keys'] = '********'
        
    return f"""
### 🔍 Session State

**Loaded Modules**:
{json.dumps(context.get('loaded_modules', []), indent=2)}

**Token Usage**:
{json.dumps(context.get('token_usage', {}), indent=2)}

**Configuration**:
```yaml
{json.dumps(safe_context.get('config', {}), indent=2)}
```
"""
```

### 5. Help & Status

```python
def show_debug_help():
    return """
### 🐞 Debug Mode Commands

- `/debug on` - Enable verbose logging
- `/debug off` - Disable verbose logging
- `/debug prompt [module]` - View system prompt for a module
- `/debug tool [name] [args]` - Test a tool in isolation
- `/debug state` - View current session state
- `/debug help` - Show this message
"""

def enable_debug_mode():
    # Set global debug flag
    # context['debug_mode'] = True
    return "✅ Debug Mode ENABLED. Verbose logging active."

def disable_debug_mode():
    # Unset global debug flag
    # context['debug_mode'] = False
    return "🚫 Debug Mode DISABLED."
```
