document.getElementById("presentation-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const topic = document.getElementById("topic").value;
    const notes = document.getElementById("notes").value;
    const readingLevel = document.getElementById("reading-level").value;

    const response = await fetch("http://localhost:8000/generate_presentation/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, notes, reading_level: readingLevel })
    });

    const result = await response.json();
    
    if (result.pdf_url) {
        document.getElementById("pdf-frame").src = `http://localhost:8000${result.pdf_url}`;
        document.getElementById("pdf-container").classList.remove("hidden");
    } else {
        alert("Error generating PDF.");
    }
});
