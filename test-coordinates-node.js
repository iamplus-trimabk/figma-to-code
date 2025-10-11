/**
 * Node.js test for LayoutConverter coordinate fix
 */

const fs = require('fs');

// Load and execute the JavaScript files
const tokenResolverCode = fs.readFileSync('./js/token-resolver.js', 'utf8');
const layoutConverterCode = fs.readFileSync('./js/layout-converter.js', 'utf8');

// Set up minimal global environment
global.window = global;
global.document = {
    createElement: () => ({ style: {} })
};

// Execute the code to define classes
eval(tokenResolverCode);
eval(layoutConverterCode);

console.log('=== TESTING COORDINATE FIX ===');

try {
    // Load design data
    const designJson = JSON.parse(fs.readFileSync('./login-screen-example.json', 'utf8'));

    // Create converter
    const converter = new LayoutConverter(designJson.designTokens);

    // Convert for mobile viewport
    const viewport = { width: 390, height: 844 };
    console.log('Viewport:', viewport);

    const renderJson = converter.convert(designJson, viewport, 'light');

    console.log('\n=== CONVERSION RESULTS ===');
    console.log('Total elements:', renderJson.elements.length);

    // Analyze each element
    renderJson.elements.forEach((element, index) => {
        console.log(`\n--- Element ${index}: ${element.id} ---`);
        console.log('Type:', element.type);
        console.log('Bounds:', element.bounds);
        console.log('Valid bounds:', element.bounds && element.bounds.x !== null && element.bounds.y !== null);

        if (element.nestedElements && element.nestedElements.length > 0) {
            console.log('Nested elements:', element.nestedElements.length);
            element.nestedElements.forEach((nested, nestedIndex) => {
                console.log(`  Nested ${nestedIndex}: ${nested.id}`);
                console.log('    Type:', nested.type);
                console.log('    Bounds:', nested.bounds);
                console.log('    Valid bounds:', nested.bounds && nested.bounds.x !== null && nested.bounds.y !== null);
            });
        }
    });

    // Write the output for debugging
    fs.writeFileSync('./test-output.json', JSON.stringify(renderJson, null, 2));
    console.log('\n=== SUCCESS ===');
    console.log('Render JSON saved to test-output.json');

    // Count valid vs invalid elements
    let totalElements = 0;
    let validElements = 0;
    let totalNestedElements = 0;
    let validNestedElements = 0;

    renderJson.elements.forEach(element => {
        totalElements++;
        if (element.bounds && element.bounds.x !== null && element.bounds.y !== null) {
            validElements++;
        }
        if (element.nestedElements) {
            element.nestedElements.forEach(nested => {
                totalNestedElements++;
                if (nested.bounds && nested.bounds.x !== null && nested.bounds.y !== null) {
                    validNestedElements++;
                }
            });
        }
    });

    console.log('\n=== VALIDATION SUMMARY ===');
    console.log(`Top-level elements: ${validElements}/${totalElements} valid`);
    console.log(`Nested elements: ${validNestedElements}/${totalNestedElements} valid`);

    if (validNestedElements === totalNestedElements) {
        console.log('✅ ALL NESTED ELEMENTS HAVE VALID COORDINATES!');
    } else {
        console.log('❌ Some nested elements still have invalid coordinates');
    }

} catch (error) {
    console.error('❌ ERROR:', error.message);
    console.error(error.stack);
}