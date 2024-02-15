function updateStateDropdown() {
    const countryDropdown = document.getElementById('country');
    const stateDropdown = document.getElementById('state');
    const selectedCountry = countryDropdown.value;

    // Clear existing state options
    stateDropdown.innerHTML = '';

    // Map of country to state options (replace with your actual data)
    const stateOptions = {
        'India': ['Kerala', 'Tamil Nadu', 'Karnataka', 'Punjab'],
        'US': ['California', 'New York', 'Alaska', 'Georgia'],
        // Add more countries and their states as needed
    };

    // Get the user's existing state value
    const userState = '{{ user.State }}';

    // Populate state options based on the selected country
    if (selectedCountry in stateOptions) {
        const states = stateOptions[selectedCountry];
        for (const state of states) {
            const option = document.createElement('option');
            option.value = state;
            option.textContent = state;
            if (state === userState) {
                option.selected = true;
            }
            stateDropdown.appendChild(option);
        }
    }
}

// Call the updateStateDropdown function to initialize the state dropdown


// Initialize the qualification counter based on the number of existing qualifications

    let qualificationCounter = 1;  // Initialize the qualification counter

    function addQualification() {
        qualificationCounter++;  // Increment the counter
        const newQualification = `
            <div class="qualification">
                <label for="qualification_${qualificationCounter}">Qualification:</label>
                <button type="button" class="add-button" onclick="addQualification()">+</button>
                <button type="button" class="remove-button" onclick="removeQualification(this)">-</button>
                <input type="text" id="qualification_${qualificationCounter}" name="qualification[]" required maxlength="20"><br><br>
                <label for="year_${qualificationCounter}">Year of Passing:</label>
                <input type="text" id="year_${qualificationCounter}" name="year[]" required><br><br>
                <label for="university_${qualificationCounter}">University:</label>
                <input type="text" id="university_${qualificationCounter}" name="university[]" required maxlength="20"><br><br>
                <label for="grade_${qualificationCounter}">Grade/Percentage:</label>
                <input type="text" id="grade_${qualificationCounter}" name="grade[]" required maxlength="20"><br><br>
            </div>
        `;
        document.getElementById('qualifications').insertAdjacentHTML('beforeend', newQualification);
    }

    function removeQualification(button) {
        const qualificationDiv = button.parentElement;
        if (qualificationCounter > 1) {
            qualificationDiv.remove();
            qualificationCounter--;
        }
    }