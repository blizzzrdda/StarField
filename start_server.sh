#!/bin/bash

echo "🚀 Starting Brotato Network Visualization Server..."
echo ""
echo "Choose your option:"
echo "1. Python HTTP Server (port 8000)"
echo "2. Node.js HTTP Server (port 8000)"
echo "3. Open embedded version directly"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Python server on http://localhost:8000"
        echo "Press Ctrl+C to stop the server"
        echo "Open http://localhost:8000/brotato_network.html in your browser"
        echo ""
        python3 -m http.server 8000 || python -m http.server 8000
        ;;
    2)
        echo ""
        echo "Starting Node.js server on http://localhost:8000"
        echo "Press Ctrl+C to stop the server"
        echo "Open http://localhost:8000/brotato_network.html in your browser"
        echo ""
        npx http-server -p 8000
        ;;
    3)
        echo ""
        echo "Opening embedded version..."
        if command -v xdg-open > /dev/null; then
            xdg-open brotato_network_embedded.html
        elif command -v open > /dev/null; then
            open brotato_network_embedded.html
        else
            echo "Please open brotato_network_embedded.html manually in your browser"
        fi
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        ;;
esac
