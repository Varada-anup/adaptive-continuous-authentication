let lastTime = Date.now();
let lastSent = 0;

function sendData(type){
    let now = Date.now();

    // limit frequency (IMPORTANT)
    if (now - lastSent < 200) return;
    lastSent = now;

    let speed = (now - lastTime)/1000;
    lastTime = now;

    fetch("/log", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            type: type,
            speed: speed,
            timestamp: now
        })
    });
}

document.addEventListener("mousemove", () => sendData("mouse"));
document.addEventListener("keydown", () => sendData("keyboard"));

setInterval(()=>{
    fetch("/detect")
    .then(res => res.json())
    .then(data => {

        let statusBox = document.getElementById("status");
        let debugBox = document.getElementById("debug");

        if(statusBox){
            statusBox.innerText = "Status: " + data.status;
        }

        if(debugBox){
            debugBox.innerText =
                "Mouse Speed: " + (data.features?.avg_mouse_speed || 0).toFixed(3) +
                "\nTyping Speed: " + (data.features?.avg_typing_speed || 0).toFixed(3) +
                "\nBaseline Mouse: " + (data.baseline?.mouse_threshold || 0).toFixed(3) +
                "\nBaseline Typing: " + (data.baseline?.typing_threshold || 0).toFixed(3);
        }

        if(data.status === "intruder"){
            alert("⚠ Suspicious behaviour detected!");
            window.location.href = "/";
        }
    });
},5000);
if (data.status === "intruder" || data.status === "logged_out") {
    captureActive = false;
    window.location = "/login";
}