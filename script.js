function startGame() {
    // In a web context, we'll redirect to level 2
    window.location.href = 'level_2.html';
}

function openOptions() {
    console.log("Opening options...");
    // You can implement options functionality here
    alert("Options menu coming soon!");
}

function quitGame() {
    // In a web context, we can either go back or close the tab
    const confirmQuit = confirm("Are you sure you want to quit?");
    if (confirmQuit) {
        window.close(); // This may not work in modern browsers
        // Fallback to returning to previous page
        window.history.back();
    }
} 