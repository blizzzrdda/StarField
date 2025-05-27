#!/usr/bin/env node

/**
 * Test Script for Brotato Network Visualization
 * Validates that all required files exist and data is properly formatted
 */

const fs = require('fs');
const path = require('path');

function testFile(filename, description) {
    try {
        const stats = fs.statSync(filename);
        const sizeKB = (stats.size / 1024).toFixed(1);
        console.log(`✅ ${description}: ${filename} (${sizeKB} KB)`);
        return true;
    } catch (error) {
        console.log(`❌ ${description}: ${filename} - NOT FOUND`);
        return false;
    }
}

function testJsonFile(filename, description, requiredFields = []) {
    try {
        const data = JSON.parse(fs.readFileSync(filename, 'utf8'));
        const sizeKB = (fs.statSync(filename).size / 1024).toFixed(1);

        // Check required fields
        const missingFields = requiredFields.filter(field => !(field in data));
        if (missingFields.length > 0) {
            console.log(`⚠️  ${description}: ${filename} (${sizeKB} KB) - Missing fields: ${missingFields.join(', ')}`);
            return false;
        }

        console.log(`✅ ${description}: ${filename} (${sizeKB} KB)`);
        return true;
    } catch (error) {
        console.log(`❌ ${description}: ${filename} - INVALID JSON or NOT FOUND`);
        return false;
    }
}

function testHtmlFile(filename, description, requiredElements = []) {
    try {
        const content = fs.readFileSync(filename, 'utf8');
        const sizeKB = (fs.statSync(filename).size / 1024).toFixed(1);

        // Check for required elements
        const missingElements = requiredElements.filter(element => !content.includes(element));
        if (missingElements.length > 0) {
            console.log(`⚠️  ${description}: ${filename} (${sizeKB} KB) - Missing: ${missingElements.join(', ')}`);
            return false;
        }

        console.log(`✅ ${description}: ${filename} (${sizeKB} KB)`);
        return true;
    } catch (error) {
        console.log(`❌ ${description}: ${filename} - NOT FOUND`);
        return false;
    }
}

function runTests() {
    console.log('🧪 Testing Brotato Network Visualization Files...\n');

    let allPassed = true;

    // Test data files
    console.log('📊 Data Files:');
    allPassed &= testJsonFile('brotato_characters.json', 'Characters Data', ['total_characters', 'characters']);
    allPassed &= testJsonFile('brotato_items.json', 'Items Data', ['total_items', 'items']);
    allPassed &= testJsonFile('brotato_network_data.json', 'Network Data', ['nodes', 'links', 'groups', 'statistics']);

    console.log('\n🔧 Processing Scripts:');
    allPassed &= testFile('process_data.js', 'Data Processor');

    console.log('\n🌐 Visualization Files:');
    allPassed &= testFile('styles.css', 'Stylesheet');
    allPassed &= testHtmlFile('brotato_network.html', 'Main Visualization', [
        'fetch(\'brotato_network_data.json\')',
        'd3.forceSimulation',
        'networkData'
    ]);

    console.log('\n🚀 Helper Scripts:');
    allPassed &= testFile('start_server.sh', 'Unix Server Script');
    allPassed &= testFile('start_server.bat', 'Windows Server Script');
    allPassed &= testFile('package.json', 'NPM Configuration');

    console.log('\n📚 Documentation:');
    allPassed &= testFile('README.md', 'Documentation');

    // Test network data structure
    console.log('\n🔍 Data Structure Validation:');
    try {
        const networkData = JSON.parse(fs.readFileSync('brotato_network_data.json', 'utf8'));

        console.log(`✅ Network Statistics:`);
        console.log(`   - Nodes: ${networkData.statistics.total_nodes}`);
        console.log(`   - Links: ${networkData.statistics.total_links}`);
        console.log(`   - Tags: ${networkData.statistics.total_tags}`);
        console.log(`   - Characters: ${networkData.statistics.total_characters} (${networkData.statistics.dlc_characters} DLC)`);
        console.log(`   - Items: ${networkData.statistics.total_items} (${networkData.statistics.dlc_items} DLC)`);
        console.log(`   - Largest Group: "${networkData.statistics.largest_group}" (${networkData.statistics.largest_group_size} nodes)`);

        // Validate data integrity
        const nodeIds = new Set(networkData.nodes.map(n => n.id));
        const invalidLinks = networkData.links.filter(l => !nodeIds.has(l.source) || !nodeIds.has(l.target));

        if (invalidLinks.length > 0) {
            console.log(`⚠️  Found ${invalidLinks.length} invalid links (referencing non-existent nodes)`);
            allPassed = false;
        } else {
            console.log(`✅ All ${networkData.links.length} links are valid`);
        }

    } catch (error) {
        console.log(`❌ Could not validate network data structure: ${error.message}`);
        allPassed = false;
    }

    // Final result
    console.log('\n' + '='.repeat(60));
    if (allPassed) {
        console.log('🎉 All tests passed! The visualization is ready to use.');
        console.log('\n🚀 Quick Start Options:');
        console.log('   1. Run: ./start_server.sh (Unix) or start_server.bat (Windows)');
        console.log('   2. Run: npx http-server -p 8000');
    } else {
        console.log('❌ Some tests failed. Please check the issues above.');
        console.log('\n🔧 To fix missing files, run:');
        console.log('   - node process_data.js (for network data)');
    }
    console.log('='.repeat(60));

    return allPassed;
}

// Run tests if called directly
if (require.main === module) {
    const success = runTests();
    process.exit(success ? 0 : 1);
}

module.exports = { runTests };
