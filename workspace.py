import os
import sys
import subprocess
import logging
from pathlib import Path
import shutil
import venv
import argparse

class FinancialNewsWorkspace:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def create_workspace(self):
        """Ustvari strukturo map in datotek."""
        try:
            # Ustvari mape
            directories = [
                'config',
                'src/data_collection',
                'src/preprocessing',
                'src/summarization',
                'src/sentiment',
                'src/visualization',
                'src/interface',
                'src/evaluation',
                'data/raw',
                'data/processed',
                'data/summaries',
                'evaluation_results',
                'tests',
                'logs'
            ]
            
            for directory in directories:
                path = self.root_dir / directory
                path.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Ustvarjena mapa: {path}")
            
            # Ustvari virtualno okolje
            venv.create(self.root_dir / 'venv', with_pip=True)
            self.logger.info("Ustvarjeno virtualno okolje")
            
        except Exception as e:
            self.logger.error(f"Napaka pri ustvarjanju delovnega okolja: {str(e)}")
            sys.exit(1)
    
    def setup_environment(self):
        """Namesti potrebne knjižnice."""
        try:
            # Namesti knjižnice
            pip_path = self.root_dir / 'venv' / 'bin' / 'pip'
            if os.name == 'nt':  # Windows
                pip_path = self.root_dir / 'venv' / 'Scripts' / 'pip'
            
            subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'])
            self.logger.info("Nameščene knjižnice iz requirements.txt")
            
        except Exception as e:
            self.logger.error(f"Napaka pri namestitvi knjižnic: {str(e)}")
            sys.exit(1)
    
    def run_application(self, mode: str = 'all'):
        """Zažene aplikacijo v izbranem načinu."""
        try:
            python_path = self.root_dir / 'venv' / 'bin' / 'python'
            if os.name == 'nt':  # Windows
                python_path = self.root_dir / 'venv' / 'Scripts' / 'python'
            
            if mode == 'all':
                subprocess.run([str(python_path), 'main.py'])
            elif mode == 'gui':
                subprocess.run([str(python_path), 'main.py', '--gui-only'])
            elif mode == 'eval':
                subprocess.run([str(python_path), 'main.py', '--eval-only'])
            
        except Exception as e:
            self.logger.error(f"Napaka pri zagonu aplikacije: {str(e)}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Financial News Analysis Workspace')
    parser.add_argument('--setup', action='store_true', help='Ustvari in nastavi delovno okolje')
    parser.add_argument('--mode', choices=['all', 'gui', 'eval'], default='all',
                       help='Način zagona aplikacije')
    
    args = parser.parse_args()
    
    workspace = FinancialNewsWorkspace()
    
    if args.setup:
        workspace.create_workspace()
        workspace.setup_environment()
    
    workspace.run_application(args.mode)

if __name__ == "__main__":
    main() 