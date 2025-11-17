@echo off
if exist .venv (call .venv\Scripts\activate)
python -m src.evaluator %*
