console.log("SCRIPT FULLY LOADED");
let currentQuery = "";
let currentPage = 1;

function cleanText(text) {
  return text
    .replace(/\r\n/g, "\n")
    .replace(/\n\s*\n/g, "<br><br>")
    .replace(/\n/g, "<br>")
    .replace(/[ \t]+/g, " ")
    .trim();
}

console.log("🔥 SCRIPT LOADED 🔥");

// 🔥 GLOBAL PARSER
function parseReference(ref) {
  const parts = ref.trim().split(" ");

  let book = "";
  let chapter = 1;
  let verse = 1;

  if (parts.length >= 2) {
    if (!isNaN(parts[0])) {
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

  return { book, chapter, verse };
}

// 📖 READ PASSAGE
window.readPassage = async function () {
  const ref = document.getElementById("readBox").value.trim();
  const version = document.getElementById("versionSelect").value;

  console.log("Reading:", ref, version);

  try {
    // 📖 Fetch Bible text
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

    // Display passage
    readingDiv.innerHTML = `
      <h3>${data.reference}</h3>
      <div class="bible-text">${cleanText(data.text)}</div>
    `;

    // Parse reference
    const parsed = parseReference(ref);

    // Fetch commentary
    const commentaryRes = await fetch(
      `/commentary?book=${encodeURIComponent(parsed.book)}&chapter=${parsed.chapter}&verse=${parsed.verse}`,
    );

    const commentaryData = await commentaryRes.json();
    console.log("COMMENTARY:", commentaryData);

    const showHenry = document.getElementById("henryToggle").checked;
    const showCalvin = document.getElementById("calvinToggle").checked;

    let commentaryHTML = "";

    if (showHenry && commentaryData.henry) {
      commentaryHTML += `
        <div class="card">
          <h3>Henry</h3>
          <p>${cleanText(commentaryData.henry)}</p>
        </div>
      `;
    }

    if (showCalvin && commentaryData.calvin) {
      commentaryHTML += `
        <div class="card">
          <h3>Calvin</h3>
          <p>${cleanText(commentaryData.calvin)}</p>
        </div>
      `;
    }

    readingDiv.innerHTML += `
      <div style="margin-top:20px; padding:10px; border-top:1px solid #ccc;">
        <h4>📘 Commentary</h4>
        ${commentaryHTML || "<p>No commentary available</p>"}
      </div>
    `;
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

// ❓ ASK AI
window.askQuestion = async function () {
  let question = document.getElementById("askBox").value;

  question = question.replace(/–/g, "-").replace(/\s+/g, " ").trim();

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
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

// Pagination
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

// Font size
let currentFontSize = 16;

window.changeFontSize = function (direction) {
  currentFontSize += direction;

  if (currentFontSize < 12) currentFontSize = 12;
  if (currentFontSize > 28) currentFontSize = 28;

  const elements = document.querySelectorAll(".bible-text, p");

  elements.forEach((el) => {
    el.style.fontSize = currentFontSize + "px";
  });
};

// Toggle listeners
document.getElementById("henryToggle").addEventListener("change", readPassage);
document.getElementById("calvinToggle").addEventListener("change", readPassage);
window.searchTheology = async function () {
  const query = document.getElementById("theologyBox").value.trim();

  console.log("THEOLOGY SEARCH:", query);

  if (!query) return;

  try {
    const res = await fetch(`/theology?query=${encodeURIComponent(query)}`);
    const data = await res.json();

    const showBerkhof = document.getElementById(
      "berkhofTheologyToggle",
    ).checked;
    const showCalvin = document.getElementById("calvinTheologyToggle").checked;

    const filtered = data.results.filter((r) => {
      if (r.source === "Berkhof" && showBerkhof) return true;
      if (r.source === "Calvin" && showCalvin) return true;
      return false;
    });

    document.getElementById("theologyResults").innerHTML =
      filtered.length > 0
        ? filtered
            .map(
              (r) => `
          <div class="card" style="margin-top:15px;">
            <strong>${r.source} – ${r.work}</strong>
            <p>${r.book}, ${r.chapter}, ${r.section}</p>
            <p>${cleanText(r.text)}</p>
          </div>
        `,
            )
            .join("")
        : "<p>No results found</p>";
  } catch (err) {
    console.error(err);
    document.getElementById("theologyResults").innerHTML =
      `<p style="color:red;">Search failed</p>`;
  }
};

// ✅ NOW add listeners AFTER function exists
document
  .getElementById("berkhofTheologyToggle")
  .addEventListener("change", searchTheology);

document
  .getElementById("calvinTheologyToggle")
  .addEventListener("change", searchTheology);
