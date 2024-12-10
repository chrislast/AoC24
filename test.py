"""Run all solutions"""
import importlib

try:
    for day in range(1,26):
        print(f"Day {day}")
        importlib.import_module(f"day{day}")
except ImportError:
    pass
