"""Main application entry point"""
import sys
import asyncio
from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from gnoman.core.splash import SplashScreen
from gnoman.core.dashboard import Dashboard
from gnoman.models.config import AppConfig
from gnoman.utils.storage import DataStore
from gnoman.utils.web3_manager import Web3Manager
from gnoman.utils.keyring_manager import KeyringManager


class GnomanApp(App):
    """GNOMAN Mission-Control Console Application"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    """
    
    TITLE = "GNOMAN Mission-Control Console"
    SUB_TITLE = "Secure Wallet & Multisig Management"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
    ]
    
    def __init__(self):
        super().__init__()
        
        # Load configuration
        self.config = AppConfig.load()
        self.config.ensure_data_dir()
        
        # Initialize managers
        self.storage = DataStore(self.config.data_dir)
        self.web3_manager = Web3Manager(self.config)
        self.keyring_manager = KeyringManager(self.config.keyring_service)
        
        # Set theme
        self.dark = self.config.theme == "dark"
    
    def on_mount(self) -> None:
        """Handle app mount"""
        # Show splash screen first
        self.push_screen(SplashScreen())
        
        # Push dashboard after splash
        self.call_later(self._show_dashboard)
    
    async def _show_dashboard(self) -> None:
        """Show the main dashboard"""
        await asyncio.sleep(3.5)  # Wait for splash to complete
        
        dashboard = Dashboard(
            self.config,
            self.storage,
            self.web3_manager,
            self.keyring_manager
        )
        self.push_screen(dashboard)
    
    def action_toggle_dark(self) -> None:
        """Toggle dark mode"""
        self.dark = not self.dark
        self.config.theme = "dark" if self.dark else "light"
        self.config.save()
    
    def action_quit(self) -> None:
        """Quit the application"""
        self.exit()


def main():
    """Main entry point"""
    try:
        app = GnomanApp()
        app.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting GNOMAN: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
