/**
 * Simple coordinate test by manually loading the classes
 */

const fs = require('fs');

console.log('=== MANUAL COORDINATE TEST ===');

// Read the JavaScript files and strip the export logic
let tokenResolverCode = fs.readFileSync('./js/token-resolver.js', 'utf8');
let layoutConverterCode = fs.readFileSync('./js/layout-converter.js', 'utf8');

// Remove the module.exports logic
tokenResolverCode = tokenResolverCode.replace(/\/\/ Export for use in other modules[\s\S]*$/, '');
layoutConverterCode = layoutConverterCode.replace(/\/\/ Export for use in other modules[\s\S]*$/, '');

// Set up global environment
global.window = global;
global.document = {
    createElement: () => ({ style: {} })
};

// Execute the code
eval(tokenResolverCode);
eval(layoutConverterCode);

console.log('Classes loaded successfully');

try {
    // Load design data
    const designJson = JSON.parse(fs.readFileSync('./login-screen-example.json', 'utf8'));
    console.log('✓ Design JSON loaded');

    // Check that we have the screen data
    if (!designJson.screens || !designJson.screens.Login) {
        console.log('❌ No Login screen found in design data');
        process.exit(1);
    }

    // Create converter with proper screen data
    const designJsonWithScreen = {
        ...designJson,
        currentScreenName: 'Login'
    };

    const converter = new LayoutConverter(designJson.designTokens);
    console.log('✓ LayoutConverter created');

    // Convert for mobile viewport
    const viewport = { width: 390, height: 844 };
    console.log('Viewport:', viewport);

    const renderJson = converter.convert(designJsonWithScreen, viewport, 'light');
    console.log('✓ Conversion completed');

    console.log('\n=== CONVERSION RESULTS ===');
    console.log('Total elements:', renderJson.elements.length);

    // Analyze each element
    let totalNestedElements = 0;
    let validNestedElements = 0;

    renderJson.elements.forEach((element, index) => {
        console.log(`\n--- Element ${index}: ${element.id} ---`);
        console.log('Type:', element.type);
        console.log('Bounds:', JSON.stringify(element.bounds));

        const isValid = element.bounds &&
                       element.bounds.x !== null && element.bounds.y !== null &&
                       element.bounds.width !== null && element.bounds.height !== null;
        console.log('Valid bounds:', isValid);

        if (element.nestedElements && element.nestedElements.length > 0) {
            console.log('Nested elements:', element.nestedElements.length);
            element.nestedElements.forEach((nested, nestedIndex) => {
                totalNestedElements++;
                console.log(`  Nested ${nestedIndex}: ${nested.id}`);
                console.log('    Type:', nested.type);
                console.log('    Bounds:', JSON.stringify(nested.bounds));

                const isNestedValid = nested.bounds &&
                                    nested.bounds.x !== null && nested.bounds.y !== null &&
                                    nested.bounds.width !== null && nested.bounds.height !== null;
                console.log('    Valid bounds:', isNestedValid);

                if (isNestedValid) {
                    validNestedElements++;
                }
            });
        }
    });

    // Write the output for debugging
    fs.writeFileSync('./test-output.json', JSON.stringify(renderJson, null, 2));
    console.log('\n✓ Render JSON saved to test-output.json');

    console.log('\n=== VALIDATION SUMMARY ===');
    console.log(`Nested elements: ${validNestedElements}/${totalNestedElements} valid`);

    if (validNestedElements === totalNestedElements && totalNestedElements > 0) {
        console.log('🎉 SUCCESS! ALL NESTED ELEMENTS HAVE VALID COORDINATES!');
        console.log('The coordinate fix is working correctly.');
    } else if (totalNestedElements === 0) {
        console.log('⚠️  No nested elements found - checking Card component structure...');

        // Debug: check if Card component exists and has children
        const cardComponent = designJson.components.Card;
        if (cardComponent) {
            console.log('Card component found:', JSON.stringify(cardComponent, null, 2));
        } else {
            console.log('❌ No Card component found in design data');
        }
    } else {
        console.log('❌ Some nested elements still have invalid coordinates');
        console.log(`${totalNestedElements - validNestedElements} elements need fixing`);
    }

} catch (error) {
    console.error('❌ ERROR:', error.message);
    console.error(error.stack);
}