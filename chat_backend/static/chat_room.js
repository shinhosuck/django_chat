window.addEventListener("DOMContentLoaded", handleWebSocket);

function handleWebSocket() {
    const url = `ws://${window.location.host}/ws/chat/room/public/`;
    const ws = new WebSocket(url);

    ws.addEventListener("open", (event) => {
        console.log("Websocket connection established");
        ws.send(JSON.stringify({ message: "new message" }));
    });

    ws.addEventListener("message", (event) => {
        const data = JSON.parse(event.data);
        console.log(data);
    });

    ws.addEventListener("close", (event) => {
        console.log("Websocket disconnected");
        console.log(event.data);
    });

    ws.addEventListener("error", (event) => {
        console.log("There was an error");
    });
}
