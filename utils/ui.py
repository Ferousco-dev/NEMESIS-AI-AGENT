"""
Rich Terminal UI System for NEMESIS
Replaces all plain print() with professional terminal UI.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn
from rich.layout import Layout
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich import box
import sys

# Global console instance
console = Console()


class NemesisUI:
    """Unified terminal UI for NEMESIS."""
    
    COLOR_SUCCESS = "green"
    COLOR_ERROR = "red"
    COLOR_WARNING = "yellow"
    COLOR_INFO = "blue"
    COLOR_SECONDARY = "cyan"
    
    @staticmethod
    def print_banner():
        """Print the NEMESIS banner with styling."""
        banner = """
[bold cyan]╔═══════════════════════════════════════════════════════╗[/]
[bold cyan]║[/bold cyan]     [bold magenta]N E M E S I S[/bold magenta]    
[bold cyan]║[/bold cyan]  [yellow]The AI Agent That Knows You Better[/yellow]  
[bold cyan]║                                                       ║[/]
[bold cyan]╚═══════════════════════════════════════════════════════╝[/]
        """
        console.print(banner)

    @staticmethod
    def panel_header(title: str, subtitle: str = None):
        """Display a header panel."""
        if subtitle:
            text = f"[bold]{title}[/bold]\n[dim]{subtitle}[/dim]"
        else:
            text = f"[bold]{title}[/bold]"
        console.print(Panel(
            text,
            border_style="cyan",
            padding=(1, 2),
            expand=False
        ))

    @staticmethod
    def panel_success(title: str, content: str):
        """Display a success panel (green)."""
        console.print(Panel(
            content,
            title=f"[bold green]✓ {title}[/bold green]",
            border_style="green",
            padding=(1, 2),
            expand=True
        ))

    @staticmethod
    def panel_error(title: str, content: str):
        """Display an error panel (red)."""
        console.print(Panel(
            content,
            title=f"[bold red]✗ {title}[/bold red]",
            border_style="red",
            padding=(1, 2),
            expand=True
        ))

    @staticmethod
    def panel_warning(title: str, content: str):
        """Display a warning panel (yellow)."""
        console.print(Panel(
            content,
            title=f"[bold yellow]⚠ {title}[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
            expand=True
        ))

    @staticmethod
    def panel_info(title: str, content: str):
        """Display an info panel (blue)."""
        console.print(Panel(
            content,
            title=f"[bold blue]ℹ {title}[/bold blue]",
            border_style="blue",
            padding=(1, 2),
            expand=True
        ))

    @staticmethod
    def panel_emphasis(content: str, title: str = None, style: str = "cyan"):
        """Display a styled panel."""
        console.print(Panel(
            content,
            title=f"[bold {style}]{title}[/bold {style}]" if title else None,
            border_style=style,
            padding=(1, 2),
            expand=True
        ))

    @staticmethod
    def status(message: str, status: str = "..."):
        """Print a status message with optional status indicator."""
        console.print(f"[cyan]{message}[/cyan] [dim]{status}[/dim]")

    @staticmethod
    def success(message: str):
        """Print a success message (green)."""
        console.print(f"[green]✓ {message}[/green]")

    @staticmethod
    def error(message: str):
        """Print an error message (red)."""
        console.print(f"[red]✗ {message}[/red]")

    @staticmethod
    def warning(message: str):
        """Print a warning message (yellow)."""
        console.print(f"[yellow]⚠ {message}[/yellow]")

    @staticmethod
    def info(message: str):
        """Print an info message (blue)."""
        console.print(f"[blue]ℹ {message}[/blue]")

    @staticmethod
    def section(title: str):
        """Print a section divider."""
        console.print(Rule(f"[bold cyan]{title}[/bold cyan]", style="cyan"))

    @staticmethod
    def table_from_dict(data: dict, title: str = None) -> Table:
        """Create a rich table from a dict."""
        table = Table(title=title, box=box.ROUNDED, border_style="cyan")
        table.add_column("Key", style="cyan", no_wrap=False)
        table.add_column("Value", style="white")
        
        for key, value in data.items():
            # Format the key
            key_text = str(key).upper().replace('_', ' ')
            # Format the value
            if isinstance(value, list):
                value_text = "\n".join(f"• {item}" for item in value)
            else:
                value_text = str(value)
            
            table.add_row(key_text, value_text)
        
        return table

    @staticmethod
    def print_dict_as_table(data: dict, title: str = None):
        """Print a dict as a formatted table."""
        table = NemesisUI.table_from_dict(data, title)
        console.print(table)

    @staticmethod
    def table_from_list(items: list, title: str = None, columns: list = None) -> Table:
        """Create a rich table from a list of dicts."""
        if not items:
            return Table(title=title)
        
        table = Table(title=title, box=box.ROUNDED, border_style="cyan")
        
        # Add columns
        if columns:
            for col in columns:
                table.add_column(col, style="cyan", no_wrap=False)
        else:
            # Infer from first item
            for col in items[0].keys():
                table.add_column(str(col).upper(), style="cyan", no_wrap=False)
        
        # Add rows
        for item in items:
            if isinstance(item, dict):
                row = [str(item.get(col, "")) for col in (columns or item.keys())]
            else:
                row = [str(item)]
            table.add_row(*row)
        
        return table

    @staticmethod
    def print_list_as_table(items: list, title: str = None, columns: list = None):
        """Print a list as a formatted table."""
        table = NemesisUI.table_from_list(items, title, columns)
        console.print(table)

    @staticmethod
    def bullet_list(items: list, title: str = None):
        """Print items as a bullet list."""
        if title:
            console.print(f"[bold cyan]{title}[/bold cyan]")
        for item in items:
            console.print(f"  [cyan]•[/cyan] {item}")

    @staticmethod
    def progress_bar(total: int, description: str = "Processing"):
        """Create a progress bar context."""
        return Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        )

    @staticmethod
    def agent_speaking(agent_name: str, content: str):
        """Display an agent's message in a styled panel."""
        titles = {
            "shadow": "[bold black]🌑 The Shadow[/bold black]",
            "profiler": "[bold magenta]🔍 The Profiler[/bold magenta]",
            "oracle": "[bold yellow]🔮 The Oracle[/bold yellow]",
            "voice": "[bold cyan]🎙️ The Voice[/bold cyan]",
        }
        
        agent_key = agent_name.lower().strip("[]")
        title = titles.get(agent_key, f"[bold]{agent_name}[/bold]")
        
        console.print(Panel(
            content,
            title=title,
            border_style="magenta",
            padding=(1, 2),
            expand=True
        ))

    @staticmethod
    def user_input_prompt(prompt: str = "You") -> str:
        """Display a styled input prompt."""
        return console.input(f"[bold cyan]{prompt}:[/bold cyan] ")

    @staticmethod
    def divider(char: str = "─", style: str = "dim"):
        """Print a visual divider."""
        console.print(f"[{style}]{char * console.width}[/{style}]")

    @staticmethod
    def clear():
        """Clear the screen."""
        console.clear()

    @staticmethod
    def print(text: str, style: str = None, **kwargs):
        """Generic print through console."""
        console.print(text, style=style, **kwargs)

    @staticmethod
    def token_counter(text: str) -> int:
        """
        Rough estimate of tokens (approx 1 token per 4 characters).
        Groq charges per 1M tokens for most models.
        """
        return len(text) // 4

    @staticmethod
    def show_token_info():
        """Display token usage optimization tips."""
        tips = """
[bold yellow]⚡ Token Usage Tips for Groq[/bold yellow]

Groq free tier has daily limits. To reduce consumption:

1. [cyan]Use lite mode:[/cyan] Set NEMESIS_MODE=lite (default)
   - Compact prompts instead of verbose ones
   - Example: [dim]NEMESIS_MODE=lite python3 main.py demo[/dim]

2. [cyan]Use smaller datasets:[/cyan]
   - Demo uses sample data (moderate tokens)
   - Your own data might be larger

3. [cyan]Reuse cached responses:[/cyan]
   - Shadow → Profiler → Oracle uses results from previous stages
   - No need to re-run if you already have profiles

4. [cyan]Batch operations:[/cyan]
   - Run analyze once, save profile
   - Run predict once, save prediction
   - Then use talk/intervene multiple times (no additional tokens)

5. [cyan]Monitor usage:[/cyan]
   Each API call shows rough tokens used
   Check Groq console: https://console.groq.com
"""
        console.print(tips)

    @staticmethod
    def show_commands_lite():
        """Show commands optimized for token usage."""
        commands = [
            "[cyan]python3 main.py ingest[/cyan] - Load data (one-time)",
            "[cyan]python3 main.py analyze[/cyan] - Build profile (saves to memory)",
            "[cyan]python3 main.py predict[/cyan] - Run predictions (saves to memory)",
            "[cyan]python3 main.py talk[/cyan] - Interact (uses cached profile, no new tokens)",
            "[cyan]python3 main.py demo[/cyan] - Full demo (uses sample data)",
        ]
        NemesisUI.bullet_list(commands, "[bold yellow]💡 Recommended Workflow[/bold yellow]")
