// PHI Detection and Masking Function (copied from upload_letter.js)
function detectAndMaskPHI(text) {
    console.log('DEBUG: Starting PHI detection and masking');
    
    let maskedText = text;
    const phiDetected = [];
    
    // Patterns for PHI detection
    const patterns = [
        // Names: Mr./Mrs./Ms./Dr. followed by name
        {
            regex: /\b(Mr\.|Mrs\.|Ms\.|Dr\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g,
            replacement: '[PATIENT_NAME]',
            type: 'name'
        },
        // UK Phone numbers
        {
            regex: /\b(?:0\d{2,4}\s?\d{3,4}\s?\d{3,4}|07\d{3}\s?\d{3}\s?\d{3})\b/g,
            replacement: '[PHONE]',
            type: 'phone'
        },
        // Email addresses
        {
            regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
            replacement: '[EMAIL]',
            type: 'email'
        },
        // UK Postcodes
        {
            regex: /\b[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][A-Z]{2}\b/g,
            replacement: '[POSTCODE]',
            type: 'postcode'
        },
        // UK Addresses (street numbers and names)
        {
            regex: /\b\d+\s+[A-Za-z\s]+(?:Street|Road|Avenue|Lane|Drive|Close|Way|Place|Court|Gardens?)\b/g,
            replacement: '[ADDRESS]',
            type: 'address'
        },
        // Hospital/Patient numbers (excluding NHS numbers)
        {
            regex: /\b(?:Hospital Number|Patient ID|MRN):\s*(\d+)\b/g,
            replacement: '[HOSPITAL_NUMBER]',
            type: 'hospital_number'
        }
    ];
    
    // Apply each pattern
    patterns.forEach(pattern => {
        const matches = maskedText.match(pattern.regex);
        if (matches) {
            maskedText = maskedText.replace(pattern.regex, pattern.replacement);
            phiDetected.push({
                type: pattern.type,
                count: matches.length,
                masked: pattern.replacement
            });
            console.log(`DEBUG: Masked ${matches.length} ${pattern.type} instances`);
        }
    });
    
    // Special handling for NHS numbers - keep them but log
    const nhsMatches = maskedText.match(/\b\d{3}\s*\d{3}\s*\d{4}\b/g);
    if (nhsMatches) {
        phiDetected.push({
            type: 'nhs_number',
            count: nhsMatches.length,
            masked: 'KEPT_FOR_CLINICAL_USE'
        });
        console.log(`DEBUG: Found ${nhsMatches.length} NHS number(s) - kept for clinical use`);
    }
    
    console.log(`DEBUG: PHI masking completed. Detected ${phiDetected.length} types of PHI`);
    
    return {
        maskedText: maskedText,
        phiDetected: phiDetected,
        originalLength: text.length,
        maskedLength: maskedText.length
    };
}

// Test the function
const testText = `15 January 2025

Mr. David Thompson
42 Oakwood Avenue
Manchester, M1 2AB
Phone: 0161 234 5678
Email: david.thompson@email.com

Dear Mr. Thompson,

Your NHS Number: 123 456 7890
Hospital Number: 98765432

This letter confirms your urgent cardiology appointment at the Cardiology Department at Manchester Royal Infirmary on Monday, 20th January 2025 at 14:30.

CLINICAL FINDINGS:
Patient presents with severe chest pain radiating to left arm and jaw, shortness of breath, diaphoresis, and lightheadedness. ECG shows ST-segment elevation in leads II, III, aVF consistent with inferior wall myocardial infarction. Troponin levels elevated at 4.2 ng/mL (normal <0.04). Blood pressure 180/110 mmHg, heart rate 120 bpm, oxygen saturation 92% on room air.

DIAGNOSIS:
Acute inferior wall myocardial infarction with cardiogenic shock.

TREATMENT PLAN:
Immediate cardiac catheterization and possible percutaneous coronary intervention (PCI). Patient requires intensive cardiac monitoring and may need intra-aortic balloon pump support.

URGENT CONCERNS:
- High risk of cardiac arrest
- Potential need for emergency bypass surgery
- Risk of ventricular arrhythmias
- Hemodynamic instability

Please bring your current medications and arrive 15 minutes early. This is an urgent appointment requiring immediate attention.

If you need to reschedule, please contact us at 0161 276 1234

Regards,
Dr. Sarah Johnson
Cardiology Department`;

console.log('=== PHI DETECTION TEST ===\n');

console.log('Original text (first 200 chars):');
console.log(testText.substring(0, 200) + '...');
console.log('\n---\n');

const result = detectAndMaskPHI(testText);

console.log('Masked text (first 200 chars):');
console.log(result.maskedText.substring(0, 200) + '...');
console.log('\n---\n');

console.log('PHI detected:');
result.phiDetected.forEach(item => {
    console.log(`- ${item.type}: ${item.count} instance(s) masked`);
});

console.log('\n---\n');
console.log('Check if "Mr. David Thompson" appears in masked text:');
console.log('Contains "Mr. David Thompson":', result.maskedText.includes('Mr. David Thompson'));
console.log('Contains "[PATIENT_NAME]":', result.maskedText.includes('[PATIENT_NAME]'));
