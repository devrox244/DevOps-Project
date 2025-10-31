// Use an async function to allow for the 'await' keyword
async function fetchAndDisplayData() {
    // 1. Get the DOM element
    const outputDiv = document.getElementById("output");
    
    // Clear the placeholder content/message
    outputDiv.innerHTML = '';

    try {
        // 2. Await the fetch call to get the HTTP Response object
        const response = await fetch("/get_data");
        
        if (!response.ok) {
            throw new Error(`Network response was not ok, status: ${response.status}`);
        }
        
        // 3. Await the response.json() call to parse the body into a JS object
        const data = await response.json();

        // 4. Update the DOM with the received data
        // NOTE: We use data.ID to match the key from your Flask jsonify function.
        const content = `
            <div class="space-y-1">
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">Name:</span> ${data.name}</p>
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">Region:</span> ${data.region}</p>
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">Temp:</span> ${data.temp}</p>
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">Time:</span> ${data.day}</p>
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">Condition:</span> ${data.condition_text}</p>
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">Feelslike:</span> ${data.feels}</p>
            </div>
        `;
        
        outputDiv.innerHTML = content;
        
    } catch (error) {
        // 5. Handle any errors during fetch or parsing
        console.error("Error fetching data:", error);
        outputDiv.innerHTML = `
            <p class="text-red-500 font-semibold">Error loading data. Check console for details.</p>
        `;
    } finally {
        // Remove the loading status regardless of success or failure
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
}

// Execute the async function when the script loads
fetchAndDisplayData();