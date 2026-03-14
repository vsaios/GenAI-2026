import { useState } from "react"
import { sendChatMessage } from "../services/api"

export default function ChatPanel() {
    const [messages, setMessages] = useState([
        { role: "bot", text: "Hi! Ask me about road safety or potholes on any Toronto street." }
    ])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleSend() {
        if (!input.trim()) return

        // Add user message to chat
        const userMsg = { role: "user", text: input }
        setMessages(prev => [...prev, userMsg])
        setInput("")
        setLoading(true)

        try {
            const data = await sendChatMessage(input)
            setMessages(prev => [...prev, { role: "bot", text: data.answer }])
        } catch (err) {
            setMessages(prev => [...prev, {
                role: "bot",
                text: "Sorry, I couldn't connect to the server. Try again."
            }])
        } finally {
            setLoading(false)
        }
    }

    function handleKeyDown(e) {
        if (e.key === "Enter") handleSend()
    }

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            height: "100%",
            padding: "16px",
            gap: "12px"
        }}>
            {/* Message history */}
            <div style={{
                flex: 1,
                overflowY: "auto",
                display: "flex",
                flexDirection: "column",
                gap: "8px"
            }}>
                {messages.map((msg, i) => (
                    <div key={i} style={{
                        alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                        background: msg.role === "user" ? "#3B8BD4" : "#f0f0f0",
                        color: msg.role === "user" ? "white" : "black",
                        padding: "10px 14px",
                        borderRadius: "12px",
                        maxWidth: "80%",
                        fontSize: "14px",
                        lineHeight: "1.5"
                    }}>
                        {msg.text}
                    </div>
                ))}
                {loading && (
                    <div style={{
                        alignSelf: "flex-start",
                        background: "#f0f0f0",
                        padding: "10px 14px",
                        borderRadius: "12px",
                        fontSize: "14px",
                        color: "#888"
                    }}>
                        Thinking...
                    </div>
                )}
            </div>

            {/* Input box */}
            <div style={{ display: "flex", gap: "8px" }}>
                <input
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask about a Toronto road..."
                    style={{
                        flex: 1,
                        padding: "10px 14px",
                        borderRadius: "8px",
                        border: "1px solid #ddd",
                        fontSize: "14px"
                    }}
                />
                <button
                    onClick={handleSend}
                    disabled={loading}
                    style={{
                        padding: "10px 18px",
                        borderRadius: "8px",
                        background: "#3B8BD4",
                        color: "white",
                        border: "none",
                        cursor: "pointer",
                        fontSize: "14px"
                    }}
                >
                    Send
                </button>
            </div>
        </div>
    )
}