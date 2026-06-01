from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yfinance as yf
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from strategy.spread import get_spread
from strategy.signals import generate_signals
from strategy.backtest import backtest_api

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_from_directory('docs', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    ticker1 = data.get('ticker1', 'MSFT')
    ticker2 = data.get('ticker2', 'GOOGL')
    start = data.get('start', '2019-01-01')
    end = data.get('end', '2023-12-31')

    s1 = yf.download(ticker1, start=start, end=end,
                     multi_level_index=False)["Close"]
    s2 = yf.download(ticker2, start=start, end=end,
                     multi_level_index=False)["Close"]

    spread, hedge_ratio = get_spread(s1, s2)
    signals = generate_signals(spread)
    result = backtest_api(signals, s1, s2, hedge_ratio)

    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)