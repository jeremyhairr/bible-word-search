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