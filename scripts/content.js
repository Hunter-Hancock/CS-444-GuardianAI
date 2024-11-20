async function testResponse() {
  chrome.runtime.sendMessage(
    {
      contentScriptQuery: 'test',
      text: "test text"
    },
    response => console.log(response)
  );
}

testResponse()
