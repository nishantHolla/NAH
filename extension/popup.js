document.getElementById("extractBtn").addEventListener("click", async () => {
  // Get the active tab
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Inject and execute the script to extract text
  chrome.scripting.executeScript(
    {
      target: { tabId: tab.id },
      function: extractText,
    },
    async (results) => {
      // Check if results exist and the result is valid
      if (results && results.length > 0 && results[0].result) {
        const query = results[0].result;
        document.getElementById("scrapedText").innerText = query; // Update the output in the popup

        // Send the extracted text to the FastAPI server via POST
        const response = await fetch("https://4715-35-240-196-135.ngrok-free.app/api/query/text", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: query }),
        });

        // Get the response from the server
        if (response.ok) {
          const result = await response.json();
          console.log(result)
          // Update the UI with the returned hashtags
          document.getElementById("hashtags").innerText = result.message;
        } else {
          document.getElementById("hashtags").innerText =
            "Failed to get hashtags.";
        }
      } else {
        document.getElementById("scrapedText").innerText =
          "Failed to extract text."; // Error case
      }

      // Inject and execute the script to extract the image (optional)
      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          function: extractImage,
        },
        (results) => {
          // Check if results exist and the result is valid
          if (results && results.length > 0 && results[0].result) {
            document.getElementById("imageContainer").src = results[0].result; // Update the output in the popup
          } else {
            document.getElementById("imageContainer").src =
              "Failed to extract image."; // Error case
          }
        }
      );
    }
  );
});

// Function that will run inside the Instagram page to extract text
function extractText() {
  // Try to find the target element (this selector is just an example, adjust as needed)
  const targetElement = document.querySelector(
    ".xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.xl565be.x5dp1im.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1w2wdq1.xen30ot.x1swvt13.x1pi30zi.xh8yej3.x5n08af>p>span"
  );
  if (targetElement) {
    const text = targetElement.textContent;
    return text; // Return the extracted text
  } else {
    return "Element not found"; // Handle case where the element is not found
  }
}

// Function that will run inside the Instagram page to extract the image (optional)
function extractImage() {
  const targetImage = document.querySelector(".x5yr21d.x11njtxf.xh8yej3 img");
  if (targetImage) {
    return targetImage.src;
  } else {
    return "Image not found";
  }
}
