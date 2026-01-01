async function sendMessage() {
  const input = document.getElementById("msg");
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: input.value})
  });

  const data = await res.json();
  if (data.error) alert(data.error);
  else document.getElementById("chat").innerHTML += `<div class="message ai">${data.reply}</div>`;
}
