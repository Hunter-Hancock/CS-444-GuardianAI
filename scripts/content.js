async function testResponse() {
  chrome.runtime.sendMessage(
    {
      contentScriptQuery: 'test',
    },
    response => console.log(response)
  );
}

testResponse()
