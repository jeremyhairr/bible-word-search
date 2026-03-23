let currentQuery = "";
let currentPage = 1;
console.log("🔥 SCRIPT LOADED 🔥");

// 📖 READ
window.readPassage = async function () {
  const ref = document.getElementById("readBox").value.trim();
  const version = document.getElementById("versionSelect").value;

  console.log("Reading:", ref, version);

  try {
    // 📖 1. Fetch Bible passage FIRST
    const res = await fetch(
      `/read?reference=${encodeURIComponent(ref)}&version=${version}`,
    );
    const data = await res.json();

    console.log("READ DATA:", data);

    const readingDiv = document.getElementById("reading");

    if (data.error) {
      readingDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
      return;
    }

    // 📘 2. Render verse FIRST
    readingDiv.innerHTML = `
            <h3>${data.reference}</h3>
            <div class="bible-text">${data.text}</div>
        `;

    // 🔍 3. Parse reference CLEANLY (FIXED)
    let book = "";
    let chapter = 1;
    let verse = 1;

    const parts = ref.trim().split(" ");

    if (parts.length >= 2) {
      // Handle books like "1 Corinthians"
      if (!isNaN(parts[0])) {
        // e.g. ["1", "Corinthians", "1:1"]
        book = (parts[0] + " " + parts[1]).toLowerCase();

        if (parts[2] && parts[2].includes(":")) {
          const cv = parts[2].split(":");
          chapter = parseInt(cv[0]);
          verse = parseInt(cv[1]);
        } else if (parts[2]) {
          chapter = parseInt(parts[2]);
          verse = 1;
        }
      } else {
        // e.g. ["John", "3:16"]
        book = parts[0].toLowerCase();

        if (parts[1] && parts[1].includes(":")) {
          const cv = parts[1].split(":");
          chapter = parseInt(cv[0]);
          verse = parseInt(cv[1]);
        } else if (parts[1]) {
          chapter = parseInt(parts[1]);
          verse = 1;
        }
      }
    }

    // 🔥 SAFETY FIX
    if (!verse || isNaN(verse)) {
      verse = 1;
    }

    if (!chapter || isNaN(chapter)) {
      chapter = 1;
    }

    console.log("Parsed:", book, chapter, verse);

    // 📘 4. Fetch commentary
    if (book && chapter && verse) {
      const commentaryRes = await fetch(
        `/commentary?book=${book}&chapter=${chapter}&verse=${verse}`,
      );

      const commentaryData = await commentaryRes.json();

      console.log("COMMENTARY:", commentaryData);

      // ➕ 5. Append commentary
      readingDiv.innerHTML += `
                <div style="margin-top:20px; padding:10px; border-top:1px solid #ccc;">
                    <h4>📘 Matthew Henry Commentary</h4>
                    ${
                      commentaryData.commentary.length > 0
                        ? commentaryData.commentary
                            .map((c) => `<p>${c}</p>`)
                            .join("")
                        : "<p>No commentary available</p>"
                    }
                </div>
            `;
    }
  } catch (err) {
    console.error("ERROR:", err);
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
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: currentQuery,
      page: currentPage,
    }),
  });

  const data = await res.json();

  document.getElementById("results").innerHTML = `
        <h3>Results (Page ${currentPage})</h3>
        ${
          data.results && data.results.length > 0
            ? data.results
                .map(
                  (r) => `
                <div style="margin-bottom:15px;">
                    <strong>${r.reference}</strong>
                    <p>${r.text}</p>
                </div>
            `,
                )
                .join("")
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
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
      }),
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
