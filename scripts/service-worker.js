chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.contentScriptQuery == "test") {

    const url = "cs-444-guardianai-production.up.railway.app"
    fetch(url).then(response => response.json())
      .then(json => sendResponse(json))

    return true;
  }
})
