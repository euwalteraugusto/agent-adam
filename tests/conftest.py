import sys
from pathlib import Path

# O código fica em src/ e usa imports diretos (ex.: `from config import ...`).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
