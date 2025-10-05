#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Function to fix syntax in generated files
function fixSyntaxInFile(filePath) {
  if (!fs.existsSync(filePath)) return;

  let content = fs.readFileSync(filePath, 'utf8');

  // Fix common syntax issues from template generation
  content = content
    // Add semicolons after closing braces before constants/variables
    .replace(/\}\s*const/g, '};\n  const')
    // Add semicolons after closing braces before return
    .replace(/\}\s*return/g, '};\n  return')
    // Add semicolons after closing braces before if statements
    .replace(/\}\s*if\s*\(/g, '};\n  if (')
    // Fix missing semicolons in variable declarations
    .replace(/(\s+const [^=]+=[^;]+)\s+(\n)/g, '$1;$2')
    // Fix missing semicolons after function calls
    .replace(/(\w+\([^)]*\))\s+(\n)/g, '$1;$2')
    // Fix missing semicolons in import/export statements
    .replace(/(export[^;]+)\s+(\n)/g, '$1;$2')
    // Fix missing semicolons in JSX props
    .replace(/([a-zA-Z]+=\{[^}]+\})\s+\n/g, '$1,\n    ')
    // Fix multiple consecutive spaces
    .replace(/  +/g, ' ')
    // Fix spacing around operators
    .replace(/([a-zA-Z])\s*=\s*{/g, '$1 = {')
    // Fix newlines and indentation
    .replace(/}\s*}/g, '}\n  }');

  fs.writeFileSync(filePath, content);
  console.log(`Fixed syntax in ${filePath}`);
}

// Fix all generated component files
const componentDirs = [
  'src/components/navigation',
  'src/components/forms',
  'src/components/display'
];

componentDirs.forEach(dir => {
  if (fs.existsSync(dir)) {
    fs.readdirSync(dir).forEach(file => {
      if (file.endsWith('.tsx')) {
        fixSyntaxInFile(path.join(dir, file));
      }
    });
  }
});

console.log('Syntax fixing complete!');