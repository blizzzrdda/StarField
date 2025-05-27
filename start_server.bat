@echo off
echo 🚀 Starting Brotato Network Visualization Server...
echo.
echo Choose your option:
echo 1. Python HTTP Server (port 8000)
echo 2. Node.js HTTP Server (port 8000)
echo 3. Open embedded version directly
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Python server on http://localhost:8000
    echo Press Ctrl+C to stop the server
    echo.
    python -m http.server 8000
) else if "%choice%"=="2" (
    echo.
    echo Starting Node.js server on http://localhost:8000
    echo Press Ctrl+C to stop the server
    echo.
    npx http-server -p 8000
) else if "%choice%"=="3" (
    echo.
    echo Opening embedded version...
    start brotato_network_embedded.html
) else (
    echo Invalid choice. Please run the script again.
)

pause
