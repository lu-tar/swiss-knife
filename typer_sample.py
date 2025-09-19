#!/usr/bin/env python3
"""
Complete Typer Blueprint - Getting Started Guide
This file demonstrates all major Typer functionalities for reference.

Installation: pip install typer rich
Usage: python typer_blueprint.py --help
"""

import typer
from typing import Optional, List
from typing_extensions import Annotated
from pathlib import Path
from enum import Enum
import json


# ============================================================================
# 1. BASIC SETUP
# ============================================================================

# Create the main app
app = typer.Typer(
    name="myapp",
    help="A comprehensive Typer application blueprint",
    add_completion=True,
    rich_markup_mode="rich"  # Enables rich formatting in help
)

# Create subcommands using Typer() groups
db_app = typer.Typer(help="Database operations")
user_app = typer.Typer(help="User management commands")
file_app = typer.Typer(help="File operations")

# Register subcommands
app.add_typer(db_app, name="db")
app.add_typer(user_app, name="user") 
app.add_typer(file_app, name="file")


# ============================================================================
# 2. ENUMS FOR CHOICES
# ============================================================================

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class OutputFormat(str, Enum):
    JSON = "json"
    YAML = "yaml"
    TABLE = "table"
    CSV = "csv"


# ============================================================================
# 3. CALLBACKS (for global options and app lifecycle)
# ============================================================================

@app.callback()
def main_callback(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Enable verbose output")] = False,
    config_file: Annotated[Optional[Path], typer.Option("--config", help="Path to config file")] = None,
    log_level: Annotated[LogLevel, typer.Option("--log-level", help="Set logging level")] = LogLevel.INFO,
):
    """
    Main application callback - runs before any command.
    Use this for global configuration, logging setup, etc.
    """
    if verbose:
        typer.echo("Verbose mode enabled")
    
    if config_file:
        typer.echo(f"Using config file: {config_file}")
        if not config_file.exists():
            typer.echo(f"Warning: Config file {config_file} not found", err=True)
    
    typer.echo(f"Log level set to: {log_level.value}")


# ============================================================================
# 4. BASIC COMMANDS WITH DIFFERENT PARAMETER TYPES
# ============================================================================

@app.command()
def hello(
    # Positional argument (required)
    name: str,
    
    # Optional argument with default
    lastname: Annotated[str, typer.Argument(help="Last name")] = "Doe",
    
    # Options with various types
    count: Annotated[int, typer.Option("--count", "-c", min=1, max=10, help="Number of greetings")] = 1,
    formal: Annotated[bool, typer.Option("--formal/--casual", help="Use formal greeting")] = False,
    caps: Annotated[bool, typer.Option("--caps", help="Use uppercase")] = False,
    
    # Option with multiple values
    languages: Annotated[List[str], typer.Option("--lang", help="Languages to greet in")] = ["english"],
):
    """
    Basic greeting command demonstrating various parameter types.
    
    Examples:
        myapp hello John --count 3 --formal --lang english --lang spanish
        myapp hello Jane Smith --caps --casual
    """
    greeting = "Good day" if formal else "Hello"
    full_name = f"{name} {lastname}"
    
    if caps:
        greeting = greeting.upper()
        full_name = full_name.upper()
    
    for _ in range(count):
        for lang in languages:
            typer.echo(f"[{lang}] {greeting}, {full_name}!")


# ============================================================================
# 5. FILE OPERATIONS
# ============================================================================

@file_app.command("read")
def read_file(
    file_path: Annotated[Path, typer.Argument(help="Path to file", exists=True, readable=True)],
    lines: Annotated[Optional[int], typer.Option("--lines", "-n", help="Number of lines to read")] = None,
    format_output: Annotated[OutputFormat, typer.Option("--format", help="Output format")] = OutputFormat.TABLE,
):
    """Read and display file contents with various options."""
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
        
        if lines:
            content = content[:lines]
            
        typer.echo(f"Reading {len(content)} lines from {file_path}")
        typer.echo(f"Output format: {format_output.value}")
        
        for i, line in enumerate(content, 1):
            typer.echo(f"{i:3}: {line.rstrip()}")
            
    except Exception as e:
        typer.echo(f"Error reading file: {e}", err=True)
        raise typer.Exit(1)


@file_app.command("create")
def create_file(
    file_path: Annotated[Path, typer.Argument(help="Path for new file")],
    content: Annotated[str, typer.Option("--content", "-c", help="File content")] = "Hello, World!",
    overwrite: Annotated[bool, typer.Option("--overwrite", help="Overwrite existing file")] = False,
):
    """Create a new file with specified content."""
    if file_path.exists() and not overwrite:
        typer.echo(f"File {file_path} already exists. Use --overwrite to replace.", err=True)
        raise typer.Exit(1)
    
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        typer.echo(f"Created file: {file_path}")
    except Exception as e:
        typer.echo(f"Error creating file: {e}", err=True)
        raise typer.Exit(1)


# ============================================================================
# 6. INTERACTIVE PROMPTS
# ============================================================================

@user_app.command("create")
def create_user(
    username: Annotated[Optional[str], typer.Option("--username", help="Username")] = None,
    email: Annotated[Optional[str], typer.Option("--email", help="Email address")] = None,
    interactive: Annotated[bool, typer.Option("--interactive", "-i", help="Interactive mode")] = False,
):
    """Create a new user with interactive prompts."""
    
    # Interactive prompts
    if interactive or not username:
        username = typer.prompt("Username")
    
    if interactive or not email:
        email = typer.prompt("Email")
    
    # Secure password prompt
    password = typer.prompt("Password", hide_input=True)
    confirm_password = typer.prompt("Confirm password", hide_input=True)
    
    if password != confirm_password:
        typer.echo("Passwords don't match!", err=True)
        raise typer.Exit(1)
    
    # Confirmation prompt
    if typer.confirm(f"Create user '{username}' with email '{email}'?"):
        typer.echo(f"✅ User '{username}' created successfully!")
    else:
        typer.echo("❌ User creation cancelled")
        raise typer.Exit()


# ============================================================================
# 7. DATABASE OPERATIONS (with progress bars)
# ============================================================================

@db_app.command("migrate")
def migrate_database(
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Show what would be done")] = False,
):
    """Run database migrations with progress indication."""
    import time
    
    migrations = ["001_create_users", "002_add_indexes", "003_add_permissions"]
    
    if dry_run:
        typer.echo("DRY RUN - Would execute:")
        for migration in migrations:
            typer.echo(f"  - {migration}")
        return
    
    # Progress bar example
    with typer.progressbar(migrations, label="Running migrations") as progress:
        for migration in progress:
            # Simulate migration work
            time.sleep(1)
            typer.echo(f"\n  Applied: {migration}")
    
    typer.echo("\n✅ All migrations completed!")


@db_app.command("backup")
def backup_database(
    output_path: Annotated[Path, typer.Argument(help="Backup output path")],
    compress: Annotated[bool, typer.Option("--compress", help="Compress backup")] = False,
    tables: Annotated[Optional[List[str]], typer.Option("--table", help="Specific tables to backup")] = None,
):
    """Create database backup."""
    typer.echo(f"Creating backup at: {output_path}")
    
    if tables:
        typer.echo(f"Backing up tables: {', '.join(tables)}")
    else:
        typer.echo("Backing up all tables")
    
    if compress:
        typer.echo("Compression enabled")
    
    # Simulate backup
    typer.echo("✅ Backup completed!")


# ============================================================================
# 8. JSON/STRUCTURED OUTPUT
# ============================================================================

@app.command("status")
def show_status(
    json_output: Annotated[bool, typer.Option("--json", help="Output as JSON")] = False,
):
    """Show application status."""
    status_data = {
        "version": "1.0.0",
        "status": "healthy",
        "uptime": "2h 34m",
        "connections": 42,
        "memory_usage": "256MB"
    }
    
    if json_output:
        typer.echo(json.dumps(status_data, indent=2))
    else:
        typer.echo("📊 Application Status:")
        for key, value in status_data.items():
            typer.echo(f"  {key.replace('_', ' ').title()}: {value}")


# ============================================================================
# 9. ERROR HANDLING AND EXIT CODES
# ============================================================================

@app.command("risky")
def risky_operation(
    fail: Annotated[bool, typer.Option("--fail", help="Force operation to fail")] = False,
):
    """Demonstrate error handling and exit codes."""
    try:
        if fail:
            raise ValueError("Simulated error occurred!")
        
        typer.echo("✅ Operation completed successfully!")
        
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        # Exit with specific error code
        raise typer.Exit(code=2)
    except Exception as e:
        typer.echo(f"💥 Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)


# ============================================================================
# 10. RICH INTEGRATION (if rich is installed)
# ============================================================================

@app.command("fancy")
def fancy_output():
    """Demonstrate rich formatting (requires 'pip install rich')."""
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.progress import track
        import time
        
        console = Console()
        
        # Rich table
        table = Table(title="Sample Data", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Name", style="cyan")
        table.add_column("Status", justify="center")
        
        table.add_row("1", "Alice", "[green]Active[/green]")
        table.add_row("2", "Bob", "[yellow]Pending[/yellow]") 
        table.add_row("3", "Charlie", "[red]Inactive[/red]")
        
        console.print(table)
        
        # Rich progress bar
        for i in track(range(5), description="Processing..."):
            time.sleep(0.5)
        
        console.print("✨ [bold green]Fancy output complete![/bold green]")
        
    except ImportError:
        typer.echo("Rich not installed. Install with: pip install rich")
        typer.echo("Basic output instead:")
        typer.echo("ID | Name    | Status")
        typer.echo("1  | Alice   | Active")
        typer.echo("2  | Bob     | Pending")
        typer.echo("3  | Charlie | Inactive")


# ============================================================================
# 11. CONTEXT AND DEPENDENCY INJECTION
# ============================================================================

@app.command("context-demo")
def context_demo(
    ctx: typer.Context,
    show_params: Annotated[bool, typer.Option("--show-params", help="Show context parameters")] = False,
):
    """Demonstrate context usage."""
    typer.echo(f"Command: {ctx.info_name}")
    typer.echo(f"Parent: {ctx.parent.info_name if ctx.parent else 'None'}")
    
    if show_params:
        typer.echo("Parameters:")
        for param, value in ctx.params.items():
            typer.echo(f"  {param}: {value}")


# ============================================================================
# 12. MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # You can also use app() instead of typer.run(app) for more control
    app()


# ============================================================================
# USAGE EXAMPLES:
# ============================================================================
"""
Basic usage:
  python typer_blueprint.py --help
  python typer_blueprint.py hello John --count 3 --formal

Subcommands:
  python typer_blueprint.py user create --interactive
  python typer_blueprint.py db migrate --dry-run
  python typer_blueprint.py file create test.txt --content "Hello World"

Advanced features:
  python typer_blueprint.py status --json
  python typer_blueprint.py fancy
  python typer_blueprint.py risky --fail

Global options:
  python typer_blueprint.py --verbose --log-level debug hello World
"""