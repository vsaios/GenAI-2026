const BASE_URL = ""

export async function sendChatMessage(message: string): Promise<{ answer: string; potholes_found: number }> {
    const response = await fetch(`${BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    if (!response.ok) throw new Error("Backend error")
    return response.json()
}

export async function getAllPotholes(): Promise<any[]> {
    const response = await fetch(`${BASE_URL}/potholes`)
    if (!response.ok) throw new Error("Backend error")
    return response.json()
}

export async function getPotholesByRoad(road: string): Promise<any[]> {
    const response = await fetch(`${BASE_URL}/potholes/${road}`)
    if (!response.ok) throw new Error("Backend error")
    return response.json()
}

export async function getSummary(): Promise<any> {
    const response = await fetch(`${BASE_URL}/summary`)
    if (!response.ok) throw new Error("Backend error")
    return response.json()
}