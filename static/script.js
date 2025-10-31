/*
Corrected JavaScript for fetching data from the Flask API.
Your original code failed because fetch() and response.json() are asynchronous 
operations that return Promises, which must be handled with .then() or async/await.
*/

// Use an async function to allow for the 'await' keyword
async function fetchAndDisplayData() {
    // 1. Get the DOM element
    const dataDiv = document.getElementById("data");
    const loadingMessage = document.getElementById("loading-status");
    
    // Clear the placeholder content/message
    dataDiv.innerHTML = '';

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
                <p class="text-lg text-gray-800"><span class="font-bold text-indigo-700">ID:</span> ${data.ID}</p>
            </div>
        `;
        
        dataDiv.innerHTML = content;
        
    } catch (error) {
        // 5. Handle any errors during fetch or parsing
        console.error("Error fetching data:", error);
        dataDiv.innerHTML = `
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