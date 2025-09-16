function App() {
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
            <div className='text-center text-gray-400'>
              <p>Chat input will go here</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
