#!/usr/bin/env node

/**
 * Create Embedded Version Generator
 * Creates a standalone HTML file with embedded network data
 */

const fs = require('fs');

function createEmbeddedVersion() {
    try {
        // Read the network data
        const networkData = JSON.parse(fs.readFileSync('brotato_network_data.json', 'utf8'));

        // Read the HTML template
        const htmlTemplate = fs.readFileSync('brotato_network.html', 'utf8');

        // Create the embedded data script
        const embeddedDataScript = `
        // Embedded network data - generated automatically
        const EMBEDDED_NETWORK_DATA = ${JSON.stringify(networkData, null, 2)};
        `;

        // Replace the init function to use embedded data
        const newInitFunction = `
        // Initialize the visualization
        async function init() {
            try {
                // Use embedded data
                networkData = EMBEDDED_NETWORK_DATA;
                console.log('Network data loaded from embedded source:', networkData);

                setupVisualization();
                populateControls();
                updateStats();
                createNetwork();

            } catch (error) {
                console.error('Error initializing visualization:', error);
                document.getElementById('stats-content').innerHTML =
                    '<p style="color: red;">Error initializing visualization. Please check the console for details.</p>';
            }
        }`;

        // Replace the fetch-based init function with embedded version
        // Find the start and end of the init function more precisely
        const initFunctionStart = htmlTemplate.indexOf('// Initialize the visualization');
        const initFunctionEnd = htmlTemplate.indexOf('// Setup the SVG and dimensions');

        if (initFunctionStart === -1 || initFunctionEnd === -1) {
            throw new Error('Could not find init function boundaries in HTML template');
        }

        let embeddedHtml = htmlTemplate.substring(0, initFunctionStart) +
                          newInitFunction + '\n\n        ' +
                          htmlTemplate.substring(initFunctionEnd);

        // Insert the embedded data script before the existing script
        embeddedHtml = embeddedHtml.replace(
            '<script>',
            `<script>${embeddedDataScript}`
        );

        // Update the title to indicate this is the embedded version
        embeddedHtml = embeddedHtml.replace(
            '<title>Brotato Characters & Items Network</title>',
            '<title>Brotato Characters & Items Network (Embedded)</title>'
        );

        // Add a note in the header
        embeddedHtml = embeddedHtml.replace(
            '<p>Interactive network showing relationships between characters and items based on shared tags</p>',
            '<p>Interactive network showing relationships between characters and items based on shared tags</p>\n            <p style="font-size: 0.9em; color: #7f8c8d;">📦 Embedded Version - No server required!</p>'
        );

        // Write the embedded version
        fs.writeFileSync('brotato_network_embedded.html', embeddedHtml);

        console.log('✅ Embedded version created successfully!');
        console.log('📁 File: brotato_network_embedded.html');
        console.log('🚀 This version can be opened directly in any browser without a server.');

        // Calculate file sizes
        const originalSize = (fs.statSync('brotato_network.html').size / 1024).toFixed(1);
        const embeddedSize = (fs.statSync('brotato_network_embedded.html').size / 1024).toFixed(1);
        const dataSize = (fs.statSync('brotato_network_data.json').size / 1024).toFixed(1);

        console.log(`\n📊 File Sizes:`);
        console.log(`   - Original HTML: ${originalSize} KB`);
        console.log(`   - Network Data: ${dataSize} KB`);
        console.log(`   - Embedded HTML: ${embeddedSize} KB`);

    } catch (error) {
        console.error('Error creating embedded version:', error);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    createEmbeddedVersion();
}

module.exports = { createEmbeddedVersion };
