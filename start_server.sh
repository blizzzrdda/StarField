#!/bin/bash

echo "🚀 Starting Brotato Network Visualization Server..."
echo ""
echo "Starting Node.js server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo "Open http://localhost:8000/brotato_network.html in your browser"
echo ""
npx http-server -p 8000
