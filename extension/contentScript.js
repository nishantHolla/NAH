// Helper function to scrape images (pre-post images, if any)
function scrapeImages() {
    let images = document.querySelectorAll('img');
    let imageData = [];
  
    images.forEach((img) => {
      // Only grab images larger than a certain size (to avoid icons)
      if (img.src && img.width > 50 && img.height > 50) { 
        imageData.push(img.src);
      }
    });
  
    return imageData.length > 0 ? imageData : null; // Return null if no valid images found
  }
  
  // Scraping text and images based on platform (Instagram, X, LinkedIn)
  function scrapeData() {
    let url = window.location.hostname;
    let text = '';
    let images = [];
    console.log(url);
    // Check the platform we're on
    if (url.includes("instagram.com")) {
      text = scrapeInstagramText();
      images = scrapeImages();
    } else if (url.includes("twitter.com") || url.includes("x.com")) {
      text = scrapeTwitterText();
      images = scrapeImages();
    } else if (url.includes("linkedin.com")) {
      text = scrapeLinkedInText();
      images = scrapeImages();
    } else {
      text = scrapeGenericText();
      images = scrapeImages();
    }
  
    // Handle cases where there is no text or images
    if (!text) text = "No caption found.";
    if (!images) images = ["No images found."];
  
    // Send scraped data back to popup or background
    chrome.runtime.sendMessage({
      type: 'scrapeData',
      images: images,
      text: text
    });
  }
  
  // Instagram-specific scraping (captions and images)
  function scrapeInstagramText() {
    let text = '';
  
    // Scrape Instagram captions (before posting)
    let captionElement = document.querySelector('textarea[aria-label="Write a caption…"]');
    if (captionElement && captionElement.value) {
      text = captionElement.value;
    }
  
    return text.trim();
  }
  
  // X (formerly Twitter)-specific scraping (captions and images)
  function scrapeTwitterText() {
    let text = '';
  
    // Scrape pre-post tweet content (text area where users type their tweet)
    let tweetElement = document.querySelector('div[data-testid="tweetTextarea_0"] div[role="textbox"]');
    if (tweetElement && tweetElement.innerText) {
      text = tweetElement.innerText;
    }
  
    return text.trim();
  }
  
  // LinkedIn-specific scraping (post captions and images)
  function scrapeLinkedInText() {
    let text = '';
  
    // Scrape text area where LinkedIn posts are being typed
    let postElement = document.querySelector('div.share-box-feed-entry__texteditor span[aria-label]');
    if (postElement && postElement.innerText) {
      text = postElement.innerText;
    }
  
    return text.trim();
  }
  
  // Generic text scraper for other platforms (pre-post captions or general text)
  function scrapeGenericText() {
    let text = '';
  
    let textElement = document.querySelector('textarea, input[type="text"], div, p');
    if (textElement && (textElement.innerText || textElement.value)) {
      text = textElement.innerText || textElement.value;
    }
  
    return text.trim();
  }
  
  // Listen for message from popup to scrape data
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'scrapeData') {
      console.log("Received message to scrape data");
      scrapeData();
    }
  });
  