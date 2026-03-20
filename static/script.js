console.log("🔥 SCRIPT CONNECTED 🔥");

window.readPassage = async function () {
    console.log("📖 readPassage triggered");

    const ref = document.getElementById("readBox").value;
    const version = document.getElementById("version").value;

    console.log("REFERENCE:", ref);
    console.log("VERSION:", version);

    try {
        const res = await fetch(`/read?reference=${encodeURIComponent(ref)}&version=${version}`);
        const data = await res.json();

        console.log("API RESPONSE:", data);

        const readingDiv = document.getElementById("reading");

        if (data.error) {
            readingDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
            return;
        }

        readingDiv.innerHTML = `
            <h3>${data.reference || "No reference returned"}</h3>
            <div>${data.text || "No text returned"}</div>
        `;
    } catch (err) {
        console.error("ERROR:", err);
        document.getElementById("reading").innerHTML =
            `<p style="color:red;">Something went wrong</p>`;
    }
};
window.startSearch = async function () {
    console.log("🔍 startSearch triggered");

    const query = document.getElementById("searchBox").value;

    try {
        const res = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        });

        const data = await res.json();

        console.log("SEARCH RESPONSE:", data);

        document.getElementById("results").innerHTML = `
            <h3>Results</h3>
            <p>${data.results}</p>
`       ;
    } catch (err) {
        console.error("SEARCH ERROR:", err);
        document.getElementById("results").innerHTML =
            `<p style="color:red;">Search failed</p>`;
    }
};
window.askQuestion = async function () {
    console.log("❓ askQuestion triggered");

    const question = document.getElementById("askBox").value;

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question: question })
        });

        const data = await res.json();

        console.log("ASK RESPONSE:", data);

        document.getElementById("askResult").innerHTML = `
            <div style="margin-top: 15px;">
                <strong>Answer:</strong>
                <p>${data.answer || "No answer returned"}</p>
            </div>
`       ;
    } 
    catch (err) {
        console.error("ASK ERROR:", err);
        document.getElementById("askResult").innerHTML =
            `<p style="color:red;">Ask failed</p>`;
    }
};
window.prevPage = function () {
    console.log("⬅ prevPage clicked");
};

window.nextPage = function () {
    console.log("➡ nextPage clicked");
};
function showSection(section) {
    document.getElementById("reading").parentElement.classList.add("hidden");
    document.getElementById("searchSection").classList.add("hidden");
    document.getElementById("askSection").classList.add("hidden");

    if (section === "read") {
        document.getElementById("reading").parentElement.classList.remove("hidden");
    } else if (section === "search") {
        document.getElementById("searchSection").classList.remove("hidden");
    } else if (section === "ask") {
        document.getElementById("askSection").classList.remove("hidden");
    }
}