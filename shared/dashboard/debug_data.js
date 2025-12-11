const fs = require('fs');
const path = require('path');
const os = require('os');

const USER_HOME = os.homedir();
const EXOCORTEX_DATA_DIR = path.join(USER_HOME, 'exocortex-data');
const ANALYSES_DIR = path.join(EXOCORTEX_DATA_DIR, 'career/analyses');

console.log('--- DEBUG INFO ---');
console.log('Home:', USER_HOME);
console.log('Exocortex Data:', EXOCORTEX_DATA_DIR);
console.log('Analyses Path:', ANALYSES_DIR);

try {
    if (fs.existsSync(ANALYSES_DIR)) {
        console.log('✅ Directory exists');
        const files = fs.readdirSync(ANALYSES_DIR);
        console.log(`Found ${files.length} files:`);
        files.slice(0, 5).forEach(f => console.log(' -', f));
        
        if (files.length > 0) {
            const firstFile = path.join(ANALYSES_DIR, files[0]);
            console.log('\nReading first file:', firstFile);
            console.log(fs.readFileSync(firstFile, 'utf-8').slice(0, 200));
        }
    } else {
        console.log('❌ Directory DOES NOT exist');
        // Try listing parent
        const parent = path.dirname(ANALYSES_DIR);
        console.log('Listing parent:', parent);
        if (fs.existsSync(parent)) {
             console.log(fs.readdirSync(parent));
        }
    }
} catch (e) {
    console.error('ERROR:', e);
}
