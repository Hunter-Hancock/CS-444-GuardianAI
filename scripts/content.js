const observer = new MutationObserver(() => {
  const emailBody = document.querySelector('div[aria-label="Message Body"]');

  if (emailBody) {
    let delay
    emailBody.addEventListener("input", () => {
      clearTimeout(delay)
      delay = setTimeout(() => {
        console.log(emailBody.innerText)

        chrome.runtime.sendMessage(
          {
            contentScriptQuery: 'test',
            text: emailBody.innerText
          },
          response => highlight(response)
        );
      }, 500)
    });

    observer.disconnect();
  }
});

observer.observe(document.body, { childList: true, subtree: true });

function highlight(response) {
  const emailBody = document.querySelector('div[aria-label="Message Body"]');

  const threshold = 0.50;

  const parts = emailBody.innerText.split(" ")

  const highlightedWords = parts.map((word) => {
    const predictions = response.predictions[word]

    const isToxic = Object.values(predictions).some(value => value > threshold);

    const filtered = Object.entries(predictions).filter(([_, value]) => value[0] > threshold).map(([key, value]) => ({ key, value: value[0] }))

    const labels = filtered.map(pred => `${pred.key}: ${pred.value.toFixed(2) * 100}%`)

    return isToxic ? `<span id="toxic-word" data-tooltip="${labels.join(", ")}">${word}</span>` : word
  })

  const newText = highlightedWords.join(" ")

  emailBody.innerHTML = newText

  const selection = window.getSelection();
  const range = document.createRange();

  range.selectNodeContents(emailBody);

  range.collapse(false);

  selection.removeAllRanges();
  selection.addRange(range);
}
