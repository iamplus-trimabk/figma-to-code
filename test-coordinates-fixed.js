/**
 * Fixed Node.js test for LayoutConverter coordinate fix
 */

const fs = require('fs');

// Load the JavaScript files
const tokenResolverCode = fs.readFileSync('./js/token-resolver.js', 'utf8');
const layoutConverterCode = fs.readFileSync('./js/layout-converter.js', 'utf8');

// Set up global environment
global.window = global;
global.document = {
    createElement: () => ({ style: {} })
};

// Execute the code
eval(tokenResolverCode);
eval(layoutConverterCode);

console.log('=== TESTING COORDINATE FIX ===');

try {
    // Load design data
    const designJson = JSON.parse(fs.readFileSync('./login-screen-example.json', 'utf8'));
    console.log('Design JSON loaded');

    // Create converter with proper screen data
    const designJsonWithScreen = {
        ...designJson,
        currentScreenName: 'Login'
    };

    const converter = new LayoutConverter(designJson.designTokens);
    console.log('LayoutConverter created');

    // Convert for mobile viewport
    const viewport = { width: 390, height: 844 };
    console.log('Viewport:', viewport);

    const renderJson = converter.convert(designJsonWithScreen, viewport, 'light');
    console.log('Conversion completed');

    console.log('\n=== CONVERSION RESULTS ===');
    console.log('Total elements:', renderJson.elements.length);

    // Analyze each element
    renderJson.elements.forEach((element, index) => {
        console.log(`\n--- Element ${index}: ${element.id} ---`);
        console.log('Type:', element.type);
        console.log('Bounds:', element.bounds);

        const isValid = element.bounds && element.bounds.x !== null && element.bounds.y !== null &&
                       element.bounds.width !== null && element.bounds.height !== null;
        console.log('Valid bounds:', isValid);

        if (element.nestedElements && element.nestedElements.length > 0) {
            console.log('Nested elements:', element.nestedElements.length);
            element.nestedElements.forEach((nested, nestedIndex) => {
                console.log(`  Nested ${nestedIndex}: ${nested.id}`);
                console.log('    Type:', nested.type);
                console.log('    Bounds:', nested.bounds);

                const isNestedValid = nested.bounds && nested.bounds.x !== null && nested.bounds.y !== null &&
                                    nested.bounds.width !== null && nested.bounds.height !== null;
                console.log('    Valid bounds:', isNestedValid);
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
        if (element.bounds && element.bounds.x !== null && element.bounds.y !== null &&
            element.bounds.width !== null && element.bounds.height !== null) {
            validElements++;
        }
        if (element.nestedElements) {
            element.nestedElements.forEach(nested => {
                totalNestedElements++;
                if (nested.bounds && nested.bounds.x !== null && nested.bounds.y !== null &&
                    nested.bounds.width !== null && nested.bounds.height !== null) {
                    validNestedElements++;
                }
            });
        }
    });

    console.log('\n=== VALIDATION SUMMARY ===');
    console.log(`Top-level elements: ${validElements}/${totalElements} valid`);
    console.log(`Nested elements: ${validNestedElements}/${totalNestedElements} valid`);

    if (validNestedElements === totalNestedElements && totalNestedElements > 0) {
        console.log('✅ ALL NESTED ELEMENTS HAVE VALID COORDINATES!');
        console.log('The coordinate fix is working correctly.');
    } else if (totalNestedElements === 0) {
        console.log('⚠️  No nested elements found - this might be an issue with the test data');
    } else {
        console.log('❌ Some nested elements still have invalid coordinates');
        console.log('The coordinate fix needs more work.');
    }

} catch (error) {
    console.error('❌ ERROR:', error.message);
    console.error(error.stack);
}