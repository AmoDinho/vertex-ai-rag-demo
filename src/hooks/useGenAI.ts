import { useState, useCallback } from 'react';
import { GoogleGenAI } from '@google/genai';
import type { ChatMessage, StreamingResponse } from '../types/chat';

export const useGenAI = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize the AI client
  const initializeAI = useCallback(() => {
    const apiKey = import.meta.env.VITE_GOOGLE_CLOUD_API_KEY;

    if (!apiKey) {
      throw new Error(
        'VITE_GOOGLE_CLOUD_API_KEY environment variable is required'
      );
    }

    const ai = new GoogleGenAI({
      apiKey: apiKey,
    });

    const model = 'gemini-2.5-flash-lite';

    const tools = [
      {
        retrieval: {
          vertexAiSearch: {
            datastore:
              'projects/genai-workloads/locations/global/collections/default_collection/dataStores/oryx-reviews_1757958334235',
          },
        },
      },
    ];

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
        },
      ],
      tools: tools,
    };

    const chat = ai.chats.create({
      model: model,
      config: generationConfig,
    });

    return chat;
  }, []);

  const sendMessage = useCallback(
    async (messageText: string) => {
      if (!messageText.trim()) return;

      setIsLoading(true);
      setError(null);

      // Add user message to chat
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        content: messageText,
        role: 'user',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);

      try {
        const chat = initializeAI();

        // Create assistant message that will be updated as we stream
        const assistantMessageId = (Date.now() + 1).toString();
        const assistantMessage: ChatMessage = {
          id: assistantMessageId,
          content: '',
          role: 'assistant',
          timestamp: new Date(),
          isStreaming: true,
        };

        setMessages((prev) => [...prev, assistantMessage]);

        // Send message and handle streaming response
        const response = await chat.sendMessageStream({
          message: [{ text: messageText }],
        });

        let fullResponse = '';

        for await (const chunk of response) {
          if (chunk.text) {
            fullResponse += chunk.text;

            // Update the assistant message with accumulated text
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? { ...msg, content: fullResponse }
                  : msg
              )
            );
          }
        }

        // Mark streaming as complete
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessageId ? { ...msg, isStreaming: false } : msg
          )
        );
      } catch (err) {
        console.error('Error sending message:', err);
        setError(
          err instanceof Error
            ? err.message
            : 'An error occurred while sending the message'
        );

        // Remove the failed assistant message
        setMessages((prev) =>
          prev.filter((msg) => msg.role === 'user' || msg.content !== '')
        );
      } finally {
        setIsLoading(false);
      }
    },
    [initializeAI]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
  };
};
