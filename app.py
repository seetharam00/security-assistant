import os

API_KEY = "sk-test-12345"   # intentionally bad, for testing the scanner

def run(cmd):
    os.system(cmd)           # Bandit should flag this