async function testResponse() {
  const text = $("body").text()
  chrome.runtime.sendMessage(
    {
      contentScriptQuery: 'test',
      text: text
    },
    response => highlight(response.text)
  );
}

testResponse()

function highlight(text) {
  console.log(text)
  $("body p").contents().each(function() {
    if (this.textContent.includes(text)) {
      const span = $('<span style="background-color: yellow; color: red;"></span>')
      span.text(this.textContent)

      $(this).replaceWith(span)
    }
  })
}

