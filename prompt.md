I want to in corporate the @google/genai package in my project. using the sdk the user should be able to send message via the textarea component and send it through the chat.sendMessageStream method dynamically, also the response from the sdk should be displayed as message in the ui.

here is a snippet of how the sdk can be used:

import { GoogleGenAI } from '@google/genai';

// Initialize Vertex with your Cloud project and location
const ai = new GoogleGenAI({
apiKey: process.env.GOOGLE_CLOUD_API_KEY,
});
const model = 'gemini-2.5-flash-lite';

const tools = [
{
retrieval: {
vertexAiSearch: {
datastore: 'projects/genai-workloads/locations/global/collections/default_collection/dataStores/oryx-reviews_1757958334235',
},
},
},
];

// Set up generation config
const generationConfig = {
maxOutputTokens: 65535,
temperature: 1,
topP: 0.95,
safetySettings: [
{
category: 'HARM_CATEGORY_HATE_SPEECH',
threshold: 'OFF',
},
{
category: 'HARM_CATEGORY_DANGEROUS_CONTENT',
threshold: 'OFF',
},
{
category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
threshold: 'OFF',
},
{
category: 'HARM_CATEGORY_HARASSMENT',
threshold: 'OFF',
}
],
tools: tools,
};

const msg4Text1 = {text: `Here are the reasons provided for the refund requests:

- Item arrived damaged, seeking refund [1, 15, 20]
- Product not as described, requesting full refund [2, 3, 10, 18]
- Wrong item received, requesting refund [4, 5, 6, 8, 11, 12, 13, 19]
- Product quality below expectations, refund requested [7, 17]
- Changed mind about purchase, want to return [9, 16]`};

const chat = ai.chats.create({
model: model,
config: generationConfig
});

async function sendMessage(message) {
const response = await chat.sendMessageStream({
message: message
});
process.stdout.write('stream result: ');
for await (const chunk of response) {
if (chunk.text) {
process.stdout.write(chunk.text);
} else {
process.stdout.write(JSON.stringify(chunk) + '\n');
}
}
}

async function generateContent() {
await sendMessage([
{text: `please tell me how many support tickets are of type REFUND`}
]);
await sendMessage([
{text: `There are 20 support tickets of type REFUND.`}
]);
await sendMessage([
{text: `please list all the refund reasons`}
]);
await sendMessage([
msg4Text1
]);
await sendMessage([
{text: `what is the average ticket duration?`}
]);
}

generateContent();
