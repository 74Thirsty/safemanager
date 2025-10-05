"""Splash screen for GNOMAN application"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Label
from textual.containers import Container, Vertical
from rich.text import Text
from rich.panel import Panel
import asyncio


GNOMAN_LOGO = """
  ██████  ███    ██  ██████  ███    ███  █████  ███    ██ 
 ██       ████   ██ ██    ██ ████  ████ ██   ██ ████   ██ 
 ██   ███ ██ ██  ██ ██    ██ ██ ████ ██ ███████ ██ ██  ██ 
 ██    ██ ██  ██ ██ ██    ██ ██  ██  ██ ██   ██ ██  ██ ██ 
  ██████  ██   ████  ██████  ██      ██ ██   ██ ██   ████ 
"""


class SplashScreen(Screen):
    """Splash screen shown during application initialization"""
    
    CSS = """
    SplashScreen {
        align: center middle;
        background: $surface;
    }
    
    #splash-container {
        width: 80;
        height: auto;
        padding: 2;
        border: heavy $primary;
        background: $panel;
    }
    
    #logo {
        text-align: center;
        color: $primary;
        text-style: bold;
    }
    
    #title {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin-top: 1;
    }
    
    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-top: 1;
    }
    
    #loading {
        text-align: center;
        color: $warning;
        margin-top: 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the splash screen layout"""
        with Container(id="splash-container"):
            yield Static(GNOMAN_LOGO, id="logo")
            yield Label("Mission-Control Console", id="title")
            yield Label("Secure Wallet & Multisig Management", id="subtitle")
            yield Label("Initializing...", id="loading")
    
    async def on_mount(self) -> None:
        """Handle screen mount"""
        loading_widget = self.query_one("#loading", Label)
        
        # Simulate loading with animation
        loading_states = [
            "Initializing...",
            "Loading configuration...",
            "Connecting to keyring...",
            "Setting up Web3 providers...",
            "Loading data stores...",
            "Ready!"
        ]
        
        for state in loading_states:
            loading_widget.update(state)
            await asyncio.sleep(0.5)
        
        # Transition to main app
        await asyncio.sleep(0.5)
        self.app.pop_screen()
