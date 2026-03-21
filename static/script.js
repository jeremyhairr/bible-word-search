let currentQuery = "";
let currentPage = 1;
console.log("🔥 SCRIPT LOADED 🔥");

// 📖 READ
window.readPassage = async function () {
    const ref = document.getElementById("readBox").value;
    const version = document.getElementById("versionSelect").value;

    console.log("Reading:", ref, version);

    try {
        const res = await fetch(`/read?reference=${encodeURIComponent(ref)}&version=${version}`);
        const data = await res.json();

        const readingDiv = document.getElementById("reading");

        if (data.error) {
            readingDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
            return;
        }

        readingDiv.innerHTML = `
            <h3>${data.reference}</h3>
            <div>${data.text}</div>
        `;
    } catch (err) {
        console.error(err);
        document.getElementById("reading").innerHTML =
            `<p style="color:red;">Error loading passage</p>`;
    }
};


// 🔍 SEARCH
window.startSearch = function () {
    currentQuery = document.getElementById("searchBox").value;
    currentPage = 1;
    loadPage();
};

    async function loadPage() {
    console.log("📄 Loading page:", currentPage);

    const res = await fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            query: currentQuery,
            page: currentPage
        })
    });

    const data = await res.json();

    document.getElementById("results").innerHTML = `
        <h3>Results (Page ${currentPage})</h3>
        ${
            data.results && data.results.length > 0
            ? data.results.map(r => `
                <div style="margin-bottom:15px;">
                    <strong>${r.reference}</strong>
                    <p>${r.text}</p>
                </div>
            `).join("")
            : "<p>No results found</p>"
        }

        <div style="margin-top:20px;">
            <button onclick="prevPage()">⬅ Prev</button>
            <button onclick="nextPage()">Next ➡</button>
        </div>
    `;
}

// ❓ ASK
window.askQuestion = async function () {
    const question = document.getElementById("askBox").value;

    console.log("Asking:", question);

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
        })
        });

        const data = await res.json();

        document.getElementById("askResult").innerHTML = `
            <div style="margin-top: 15px;">
                <strong>Answer:</strong>
                <p>${data.answer}</p>
            </div>
        `;
    } catch (err) {
        console.error(err);
        document.getElementById("askResult").innerHTML =
            `<p style="color:red;">Ask failed</p>`;
    }
};
window.nextPage = function () {
    currentPage++;
    loadPage();
};

window.prevPage = function () {
    if (currentPage > 1) {
        currentPage--;
        loadPage();
    }
};