# 🥔 Brotato Characters & Items Network Visualization

An interactive network visualization showing relationships between Brotato characters and items based on shared tags, inspired by the [D3 Disjoint Force-Directed Graph](https://observablehq.com/@d3/disjoint-force-directed-graph/2).

## 🌟 Features

- **Interactive Force-Directed Graph**: Characters and items are connected based on shared tags
- **Multiple Tag Support**: Nodes can belong to multiple groups simultaneously
- **Visual Distinction**:
  - 🟢 Green circles = Characters
  - 🔵 Blue circles = Items
  - 🟠 Orange outline = DLC content
- **Advanced Filtering**:
  - Filter by node type (characters/items)
  - Filter by DLC status
  - Filter by specific tags
- **Interactive Controls**:
  - Drag nodes to reposition
  - Zoom and pan
  - Toggle labels on/off
  - Hover for detailed information
- **Real-time Statistics**: Live network statistics and group information

## 📊 Network Statistics

- **Total Nodes**: 286 (62 characters + 224 items)
- **Total Connections**: 3,866 links based on shared tags
- **Tags**: 32 unique gameplay tags
- **Largest Group**: "Max HP" with 33 connected nodes
- **DLC Content**: 14 characters and 32 items

## 🚀 Quick Start

### Prerequisites

- Node.js (for data processing)
- Modern web browser with JavaScript enabled

### Setup

1. **Process the data** (if not already done):
   ```bash
   node process_data.js
   ```

2. **Choose your viewing method**:

   **🎯 Easiest Option - Embedded Version:**
   ```bash
   # Open directly in browser (no server needed)
   open brotato_network_embedded.html
   ```

   **🚀 Server Options (for full features):**
   ```bash
   # Option A: Use the helper scripts
   ./start_server.sh        # Linux/Mac
   start_server.bat         # Windows

   # Option B: Manual server start
   python -m http.server 8000
   # Then open: http://localhost:8000/brotato_network.html

   # Option C: Node.js server
   npx http-server -p 8000
   # Then open: http://localhost:8000/brotato_network.html
   ```

### Usage

1. **Navigation**:
   - **Drag**: Click and drag nodes to reposition them
   - **Zoom**: Use mouse wheel or pinch to zoom in/out
   - **Pan**: Click and drag empty space to pan around

2. **Filtering**:
   - Use the dropdown menus to filter by type, DLC status, or specific tags
   - Filters work in combination for precise control

3. **Information**:
   - **Hover** over any node to see detailed information
   - **Statistics panel** shows live network metrics
   - **Legend** explains the color coding

## 🏗️ File Structure

```
├── brotato_characters.json         # Character data (62 characters)
├── brotato_items.json              # Item data (224 items)
├── process_data.js                 # Data processing script
├── create_embedded_version.js      # Creates standalone HTML file
├── brotato_network_data.json       # Generated network data
├── brotato_network.html            # Main visualization (needs server)
├── brotato_network_embedded.html   # Standalone version (no server needed)
├── styles.css                      # Styling and responsive design
├── start_server.sh                 # Helper script for Unix systems
├── start_server.bat                # Helper script for Windows
├── package.json                    # Node.js project configuration
└── README.md                       # This file
```

### File Descriptions

- **`brotato_network.html`**: Full-featured version that loads data via HTTP
- **`brotato_network_embedded.html`**: Standalone version with embedded data (616KB)
- **`process_data.js`**: Processes raw JSON data into network format
- **`create_embedded_version.js`**: Generates the embedded HTML version
- **Helper scripts**: Easy server startup for different platforms

## 🔧 Technical Details

### Data Processing

The `process_data.js` script:
1. Loads character and item data from JSON files
2. Extracts all unique tags (32 total)
3. Creates nodes for each character and item
4. Generates links between nodes sharing tags
5. Creates groups based on tag relationships
6. Outputs processed data to `brotato_network_data.json`

### Visualization Technology

- **D3.js v7**: Force-directed graph simulation
- **HTML5/CSS3**: Responsive design and modern styling
- **Vanilla JavaScript**: No additional frameworks required

### Force Simulation Parameters

- **Link Distance**: 50px (adjustable based on shared tag count)
- **Charge Strength**: -100 (repulsion between nodes)
- **Collision Detection**: 15px radius to prevent overlap
- **Center Force**: Keeps nodes centered in viewport

## 🎯 Tag Categories

The network groups nodes by these tag categories:

### Damage Types
- **Melee Damage** (19 nodes)
- **Ranged Damage** (15 nodes)
- **Elemental Damage** (8 nodes)

### Defensive Stats
- **Max HP** (33 nodes) - Largest group
- **Armor** (11 nodes)
- **Dodge** (8 nodes)
- **HP Regeneration** (13 nodes)

### Utility & Economy
- **Engineering** (8 nodes)
- **Harvesting** (12 nodes)
- **Luck** (14 nodes)
- **Speed** (9 nodes)

### Special Mechanics
- **Consumable** (8 nodes)
- **Structure** (6 nodes)
- **Explosive** (5 nodes)
- **Curse** (4 nodes)

## 🎮 Insights from the Network

1. **Max HP is Central**: The largest connected group, showing HP is a core mechanic
2. **Damage Type Clusters**: Clear separation between melee, ranged, and elemental builds
3. **DLC Integration**: DLC content is well-integrated across all tag categories
4. **Character Specialization**: Characters tend to have fewer but more focused tags
5. **Item Diversity**: Items often bridge multiple tag categories

## 🔄 Updating Data

To update the visualization with new game data:

1. Update `brotato_characters.json` and/or `brotato_items.json`
2. Run the data processor: `node process_data.js`
3. Refresh the browser to see updated visualization

## 🎨 Customization

### Colors
Edit the color scales in `brotato_network.html`:
```javascript
const colorScale = d3.scaleOrdinal()
    .domain(['character', 'item'])
    .range(['#4CAF50', '#2196F3']); // Green, Blue
```

### Layout
Modify force simulation parameters:
```javascript
.force('link', d3.forceLink(links).distance(50).strength(0.1))
.force('charge', d3.forceManyBody().strength(-100))
```

### Styling
Customize appearance in `styles.css` - fully responsive design included.

## 📱 Browser Compatibility

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

## 🤝 Contributing

Feel free to enhance the visualization:
- Add new filtering options
- Improve the layout algorithm
- Add animation effects
- Enhance mobile responsiveness

## 📄 License

This project uses data from the Brotato Wiki and is intended for educational and analysis purposes.

---

**Enjoy exploring the Brotato universe! 🥔✨**
