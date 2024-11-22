chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.contentScriptQuery == "test") {

    //const url = `https://cs-444-guardianai-production.up.railway.app?text=${request.text}`
    const url = `http://127.0.0.1:5000`
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: request.text })
    }).then(response => response.json())
      .then(json => sendResponse(json))

    return true;
  }
})
