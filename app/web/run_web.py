import streamlit.web.cli as stcli
import sys

def main():
    sys.argv = ["streamlit", "run", "app/web/app.py"]
    stcli.main()
