console.log("🔥 SCRIPT CONNECTED 🔥");

// 📖 READ PASSAGE
window.readPassage = async function () {
    console.log("📖 readPassage triggered");

    const ref = document.getElementById("readBox").value;
    const version = document.getElementById("versionSelect").value;

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
    }
};


// 🔍 SEARCH
window.startSearch = async function () {
    console.log("🔍 startSearch triggered");

    const query = document.getElementById("searchBox").value;

    try {
        const res = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query })
        });

        const data = await res.json();

        document.getElementById("results").innerHTML = `
            <h3>Results</h3>
            ${
                data.results && data.results.length
                    ? data.results.map(r => `
                        <div>
                            <strong>${r.reference}</strong>
                            <p>${r.text}</p>
                        </div>
                    `).join("")
                    : "<p>No results</p>"
            }
        `;
    } catch (err) {
        console.error(err);
    }
};


// ❓ ASK AI
window.askQuestion = async function () {
    console.log("❓ ask triggered");

    const question = document.getElementById("askBox").value;

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await res.json();

        document.getElementById("askResult").innerHTML = `
            <strong>Answer:</strong>
            <p>${data.answer}</p>
        `;
    } catch (err) {
        console.error(err);
    }
};


// 🔁 TAB SWITCH
window.showSection = function (section) {
    document.getElementById("readSection").style.display = "none";
    document.getElementById("searchSection").style.display = "none";
    document.getElementById("askSection").style.display = "none";

    document.getElementById(section).style.display = "block";
};


// ⬅ ➡ PAGINATION (placeholder)
window.prevPage = function () {
    console.log("⬅ prev");
};

window.nextPage = function () {
    console.log("➡ next");
};