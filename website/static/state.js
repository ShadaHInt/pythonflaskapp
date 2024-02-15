function updateStateDropdown() {

    const countrySelect = document.getElementById("country");

    const stateSelect = document.getElementById("state");

    const selectedCountry = countrySelect.value;

    stateSelect.innerHTML = ""; // Clear previous options

    if (selectedCountry === "India") {

        const states = ["Kerala","Tamil Nadu", "Karnataka", "Punjab"];

        for (const state of states) {

            const option = document.createElement("option");

            option.value = state;

            option.textContent = state;

            stateSelect.appendChild(option);

        }

    } else if (selectedCountry === "US") {

        const states = ["California", "New York", "Alaska", "Georgia"];

        for (const state of states) {

            const option = document.createElement("option");

            option.value = state;

            option.textContent = state;

            stateSelect.appendChild(option);

        }

    }

}

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