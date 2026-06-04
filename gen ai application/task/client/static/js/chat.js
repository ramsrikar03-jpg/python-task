async function sendMessage() {

    const input = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();

    if (!message) return;

    const safeMessage = message
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    chatBox.innerHTML += `
        <div class="user-message">
            ${safeMessage}
        </div>
    `;

    input.value = "";

    chatBox.innerHTML += `
        <div class="bot-message" id="typing">
            Typing...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    document.getElementById("typing").remove();

    const safeResponse = String(data.response)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "<br>");

    chatBox.innerHTML += `
        <div class="bot-message">
            ${safeResponse}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}

document
    .getElementById("message")
    .addEventListener("keypress", function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }
    });