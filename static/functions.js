async function copyShare() {
    const button = document.getElementById("copy-link");

    try {
        if (navigator.share) {
            // Open the share sheet on mobile
            navigator.share({
                title: document.title,
                url: window.location.href,
            });
        } else if (navigator.clipboard) {
            // copy the page URL to the clipboard
            await navigator.clipboard.writeText(window.location.href);
        } else {
            // Fallback for older browsers / insecure contexts
            const input = document.createElement("textarea");
            input.value = window.location.href;
            document.body.appendChild(input);
            input.select();
            document.execCommand("copy");
            document.body.removeChild(input);
        }

        button.textContent = "Link Copied!";
    } catch (err) {
        console.error(err);
        button.textContent = "Copy Failed";
    }

    setTimeout(() => {
        button.textContent = "Share";
    }, 2000);
}
