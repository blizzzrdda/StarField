#!/usr/bin/env node

/**
 * Brotato Network Data Processor
 * Processes character and item data to create a network graph structure
 * for D3.js force-directed visualization
 */

const fs = require('fs');
const path = require('path');

// Load data files
function loadData() {
    try {
        const charactersData = JSON.parse(fs.readFileSync('brotato_characters.json', 'utf8'));
        const itemsData = JSON.parse(fs.readFileSync('brotato_items.json', 'utf8'));
        
        return {
            characters: charactersData.characters,
            items: itemsData.items
        };
    } catch (error) {
        console.error('Error loading data files:', error);
        process.exit(1);
    }
}

// Extract all unique tags from both datasets
function extractAllTags(characters, items) {
    const tagSet = new Set();
    
    // Add character tags
    characters.forEach(character => {
        character.tags.forEach(tag => tagSet.add(tag));
    });
    
    // Add item tags
    items.forEach(item => {
        item.tags.forEach(tag => tagSet.add(tag));
    });
    
    return Array.from(tagSet).sort();
}

// Create nodes for the network
function createNodes(characters, items, allTags) {
    const nodes = [];
    let nodeId = 0;
    
    // Create character nodes
    characters.forEach(character => {
        nodes.push({
            id: nodeId++,
            name: character.name,
            type: 'character',
            tags: character.tags,
            is_dlc: character.is_dlc,
            stats: character.stats,
            unlocked_by: character.unlocked_by,
            unlocks: character.unlocks
        });
    });
    
    // Create item nodes
    items.forEach(item => {
        nodes.push({
            id: nodeId++,
            name: item.name,
            type: 'item',
            tags: item.tags,
            is_dlc: item.is_dlc,
            rarity: item.rarity,
            effects: item.effects,
            base_price: item.base_price,
            limit: item.limit,
            unlocked_by: item.unlocked_by
        });
    });
    
    return nodes;
}

// Create links between nodes that share tags
function createLinks(nodes) {
    const links = [];
    const linkSet = new Set(); // To avoid duplicate links
    
    // Create links between nodes that share at least one tag
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            const nodeA = nodes[i];
            const nodeB = nodes[j];
            
            // Find shared tags
            const sharedTags = nodeA.tags.filter(tag => nodeB.tags.includes(tag));
            
            if (sharedTags.length > 0) {
                const linkId = `${Math.min(nodeA.id, nodeB.id)}-${Math.max(nodeA.id, nodeB.id)}`;
                
                if (!linkSet.has(linkId)) {
                    linkSet.add(linkId);
                    links.push({
                        source: nodeA.id,
                        target: nodeB.id,
                        shared_tags: sharedTags,
                        strength: sharedTags.length // Link strength based on number of shared tags
                    });
                }
            }
        }
    }
    
    return links;
}

// Create groups based on tags
function createGroups(allTags, nodes) {
    const groups = allTags.map((tag, index) => {
        const nodesInGroup = nodes.filter(node => node.tags.includes(tag));
        
        return {
            id: index,
            name: tag,
            nodes: nodesInGroup.map(node => node.id),
            character_count: nodesInGroup.filter(node => node.type === 'character').length,
            item_count: nodesInGroup.filter(node => node.type === 'item').length,
            total_count: nodesInGroup.length
        };
    });
    
    // Filter out empty groups and sort by size
    return groups
        .filter(group => group.total_count > 0)
        .sort((a, b) => b.total_count - a.total_count);
}

// Generate statistics
function generateStats(characters, items, nodes, links, groups, allTags) {
    const characterTags = new Set();
    const itemTags = new Set();
    
    characters.forEach(char => char.tags.forEach(tag => characterTags.add(tag)));
    items.forEach(item => item.tags.forEach(tag => itemTags.add(tag)));
    
    return {
        total_characters: characters.length,
        total_items: items.length,
        total_nodes: nodes.length,
        total_links: links.length,
        total_tags: allTags.length,
        character_only_tags: Array.from(characterTags).filter(tag => !itemTags.has(tag)).length,
        item_only_tags: Array.from(itemTags).filter(tag => !characterTags.has(tag)).length,
        shared_tags: Array.from(characterTags).filter(tag => itemTags.has(tag)).length,
        dlc_characters: characters.filter(char => char.is_dlc).length,
        dlc_items: items.filter(item => item.is_dlc).length,
        largest_group: groups[0]?.name || 'None',
        largest_group_size: groups[0]?.total_count || 0
    };
}

// Main processing function
function processData() {
    console.log('Loading Brotato data...');
    const { characters, items } = loadData();
    
    console.log('Extracting tags...');
    const allTags = extractAllTags(characters, items);
    
    console.log('Creating nodes...');
    const nodes = createNodes(characters, items, allTags);
    
    console.log('Creating links...');
    const links = createLinks(nodes);
    
    console.log('Creating groups...');
    const groups = createGroups(allTags, nodes);
    
    console.log('Generating statistics...');
    const stats = generateStats(characters, items, nodes, links, groups, allTags);
    
    // Create the final network data structure
    const networkData = {
        metadata: {
            generated_at: new Date().toISOString(),
            source_files: ['brotato_characters.json', 'brotato_items.json'],
            description: 'Network graph data for Brotato characters and items grouped by tags'
        },
        statistics: stats,
        nodes: nodes,
        links: links,
        groups: groups,
        tags: allTags
    };
    
    // Save the processed data
    const outputFile = 'brotato_network_data.json';
    fs.writeFileSync(outputFile, JSON.stringify(networkData, null, 2));
    
    console.log(`\n✅ Network data processed successfully!`);
    console.log(`📊 Statistics:`);
    console.log(`   - Characters: ${stats.total_characters} (${stats.dlc_characters} DLC)`);
    console.log(`   - Items: ${stats.total_items} (${stats.dlc_items} DLC)`);
    console.log(`   - Total nodes: ${stats.total_nodes}`);
    console.log(`   - Total links: ${stats.total_links}`);
    console.log(`   - Total tags: ${stats.total_tags}`);
    console.log(`   - Largest group: "${stats.largest_group}" (${stats.largest_group_size} nodes)`);
    console.log(`\n📁 Output saved to: ${outputFile}`);
    
    return networkData;
}

// Run if called directly
if (require.main === module) {
    processData();
}

module.exports = { processData };
