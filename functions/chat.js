export async function onRequest(context) {
  const { request } = context;
  const body = await request.json();
  const GROQ_KEY = context.env.GROQ_API_KEY;

  const groqRes = await fetch("https://api.groq.com/openai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${GROQ_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "llama-3.3-70b-versatile",
      messages: body.messages
    })
  });

  const data = await groqRes.json();
  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" }
  });
}