export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  isStreaming?: boolean;
}

export interface StreamingResponse {
  text?: string;
  functionCall?: any;
  candidates?: any[];
}

export interface GenAIConfig {
  apiKey: string;
  model: string;
  maxOutputTokens: number;
  temperature: number;
  topP: number;
}
