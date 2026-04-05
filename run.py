"""
簡化版：不需依賴 Ollama
直接啟動 Flask Web 應用
"""

from app import app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
