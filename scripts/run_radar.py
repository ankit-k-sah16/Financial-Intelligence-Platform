from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.analytics.radar import RadarChartGenerator

if __name__ == "__main__":

    RadarChartGenerator().run()