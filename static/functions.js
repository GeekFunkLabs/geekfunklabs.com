function copyShare() {
    navigator.clipboard.writeText(window.location.href);

    var elem = document.getElementById("copy-link");
    elem.innerHTML = "Link Copied!";
    
    setTimeout(() => {elem.innerHTML = "Share"}, 2000);
}

