import { useState } from 'react';
import { Send } from 'lucide-react';

function App() {
  const [message, setMessage] = useState('');

  const handleSendMessage = () => {
    if (message.trim()) {
      // TODO: Send message to model
      console.log('Sending message:', message.trim());
      setMessage('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className='min-h-screen bg-gradient-to-br from-[#80ded9] via-[#aeecef] to-[#fffaff] flex flex-col'>
      {/* Chat App Container */}
      <div className='flex-1 flex flex-col max-w-4xl mx-auto w-full p-4'>
        {/* Header */}
        <header className='mb-6'>
          <h1 className='text-3xl font-bold text-gray-800 text-center'>
            Chat App
          </h1>
        </header>

        {/* Chat Interface Container */}
        <div className='flex-1 flex flex-col bg-white/80 backdrop-blur-sm rounded-xl shadow-lg border border-white/20'>
          {/* Chat Messages Area */}
          <div className='flex-1 p-6'>
            <div className='text-center text-gray-500 mt-12'>
              <p>Welcome to your chat app!</p>
              <p className='text-sm mt-2'>Messages will appear here</p>
            </div>
          </div>

          {/* Chat Input Area */}
          <div className='p-6 border-t border-gray-200/50'>
            <div className='relative'>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder='Type your message here... (Press Enter to send, Shift+Enter for new line)'
                className='w-full resize-none rounded-lg border border-gray-300 bg-white/90 px-4 py-3 pr-14 text-gray-800 placeholder-gray-500 shadow-sm transition-all duration-200 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 min-h-[44px] max-h-32 overflow-y-auto'
                rows={1}
                style={{
                  minHeight: '44px',
                  height: message
                    ? Math.min(
                        Math.max(44, message.split('\n').length * 24 + 20),
                        128
                      ) + 'px'
                    : '44px',
                }}
              />
              <button
                onClick={handleSendMessage}
                disabled={!message.trim()}
                className='absolute right-2 top-1/2 -translate-y-1/2 flex h-8 w-8 items-center justify-center rounded-md bg-blue-500 text-white transition-all duration-200 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:bg-gray-300 disabled:cursor-not-allowed'
                aria-label='Send message'
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
