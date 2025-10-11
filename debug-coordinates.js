/**
 * Debug script to test LayoutConverter coordinate calculation
 */

// Load required modules
const fs = require('fs');

// Mock browser environment
global.window = global;
global.document = {
    createElement: () => ({ style: {} })
};

// Load the LayoutConverter
const layoutConverterCode = fs.readFileSync('./js/layout-converter.js', 'utf8');
const tokenResolverCode = fs.readFileSync('./js/token-resolver.js', 'utf8');

eval(tokenResolverCode);
eval(layoutConverterCode);

// Load the design JSON
const designJson = JSON.parse(fs.readFileSync('./login-screen-example.json', 'utf8'));

console.log('=== DEBUG LAYOUT CONVERTER ===');
console.log('Design JSON loaded successfully');
console.log('Screen:', designJson.screens.Login.name);
console.log('Children count:', designJson.screens.Login.children.length);

// Create LayoutConverter instance
const converter = new LayoutConverter(designJson.designTokens);

// Test conversion for mobile viewport
const viewport = { width: 390, height: 844 };
console.log('\n=== CONVERTING TO RENDER JSON ===');
console.log('Viewport:', viewport);

const renderJson = converter.convert(designJson, viewport, 'light');

console.log('\n=== RENDER JSON ANALYSIS ===');
console.log('Total elements:', renderJson.elements.length);

renderJson.elements.forEach((element, index) => {
    console.log(`\nElement ${index}: ${element.id}`);
    console.log(`  Type: ${element.type}`);
    console.log(`  Bounds:`, element.bounds);
    console.log(`  Has nested elements:`, !!element.nestedElements);

    if (element.nestedElements && element.nestedElements.length > 0) {
        console.log(`  Nested elements count: ${element.nestedElements.length}`);
        element.nestedElements.forEach((nested, nestedIndex) => {
            console.log(`    Nested ${nestedIndex}: ${nested.id}`);
            console.log(`      Type: ${nested.type}`);
            console.log(`      Bounds:`, nested.bounds);
            console.log(`      Valid bounds: ${nested.bounds && nested.bounds.x !== null && nested.bounds.y !== null && nested.bounds.width !== null && nested.bounds.height !== null}`);
        });
    }
});

// Write debug output to file
fs.writeFileSync('./debug-output.json', JSON.stringify(renderJson, null, 2));
console.log('\n=== DEBUG OUTPUT ===');
console.log('Full render JSON written to debug-output.json');