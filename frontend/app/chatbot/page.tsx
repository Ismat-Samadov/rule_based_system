'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, Sparkles, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import clsx from 'clsx';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

interface Message {
  id: string;
  role: 'user' | 'bot';
  content: string;
  timestamp: Date;
  quickReplies?: string[];
}

interface ChatResponse {
  intent: string;
  confidence: number;
  response: string;
  action?: string;
  quick_replies?: string[];
  entities?: Record<string, any>;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const INITIAL_SUGGESTIONS = [
  '💧 Buğdanı nə vaxt suvarmalıyam?',
  '🌿 Pomidora hansı gübrə lazımdır?',
  '🐛 Yarpaqlar niyə saraldı?',
  '🌡️ İsti havada nə etməliyəm?',
  '🐄 İnəyi necə yemləməliyəm?',
];

export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'bot',
      content: 'Salam! Mən AgriAdvisor - sizin kənd təsərrüfatı məsləhətçinizəm. Suvarma, gübrələmə, zərərverici və ya digər mövzularda sual verə bilərsiniz. 🌾\n\nBuradan başlaya bilərsiniz:',
      timestamp: new Date(),
      quickReplies: INITIAL_SUGGESTIONS,
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/v1/chat/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) throw new Error('API error');

      const data: ChatResponse = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: data.response,
        timestamp: new Date(),
        quickReplies: data.quick_replies,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: 'Bağışlayın, texniki xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickReply = (reply: string) => {
    sendMessage(reply);
  };

  const formatMessage = (content: string) => {
    // Convert markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br />');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-earth-50 to-white">
      <Header />

      <main className="flex-1 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-6">
            <Link href="/" className="inline-flex items-center gap-2 text-earth-600 hover:text-leaf-600 transition-colors mb-4">
              <ArrowLeft className="w-4 h-4" />
              Ana səhifəyə qayıt
            </Link>
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-leaf-500 to-leaf-600 rounded-2xl flex items-center justify-center shadow-lg">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-display font-bold text-earth-900 mb-1">AgriAdvisor Məsləhətçi</h1>
                <p className="text-earth-600 flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Online - Kənd təsərrüfatı üzrə AI köməkçi
                </p>
              </div>
            </div>
          </div>

          {/* Chat Container */}
          <div className="card overflow-hidden shadow-lg border-2 border-leaf-100">
            {/* Messages */}
            <div className="h-[600px] overflow-y-auto p-6 space-y-6">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={clsx(
                    'flex gap-3 animate-fade-in',
                    message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                  )}
                >
                  {/* Avatar */}
                  <div className={clsx(
                    'w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center shadow-sm',
                    message.role === 'user'
                      ? 'bg-gradient-to-br from-sky-400 to-sky-500'
                      : 'bg-gradient-to-br from-leaf-400 to-leaf-500'
                  )}>
                    {message.role === 'user' ? (
                      <User className="w-5 h-5 text-white" />
                    ) : (
                      <Bot className="w-5 h-5 text-white" />
                    )}
                  </div>

                  <div className="flex-1 max-w-[75%]">
                    {/* Message bubble */}
                    <div className={clsx(
                      'rounded-2xl px-5 py-3 shadow-sm',
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-sky-500 to-sky-600 text-white rounded-br-md'
                        : 'bg-white border-2 border-earth-100 text-earth-700 rounded-bl-md'
                    )}>
                      <div
                        className="text-sm leading-relaxed"
                        dangerouslySetInnerHTML={{ __html: formatMessage(message.content) }}
                      />
                      <div className={clsx(
                        'text-xs mt-2',
                        message.role === 'user' ? 'text-sky-100' : 'text-earth-400'
                      )}>
                        {message.timestamp.toLocaleTimeString('az-AZ', { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>

                    {/* Quick replies */}
                    {message.quickReplies && message.quickReplies.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {message.quickReplies.map((reply, idx) => (
                          <button
                            key={idx}
                            onClick={() => handleQuickReply(reply)}
                            className="px-4 py-2 text-sm bg-leaf-50 text-leaf-700 border border-leaf-200 rounded-full hover:bg-leaf-100 hover:border-leaf-300 transition-all shadow-sm"
                          >
                            {reply}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Loading indicator */}
              {loading && (
                <div className="flex gap-3 animate-fade-in">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-leaf-400 to-leaf-500 flex items-center justify-center shadow-sm">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                  <div className="bg-white border-2 border-earth-100 rounded-2xl rounded-bl-md px-5 py-4 shadow-sm">
                    <div className="flex gap-1.5">
                      <span className="w-2.5 h-2.5 bg-leaf-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                      <span className="w-2.5 h-2.5 bg-leaf-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                      <span className="w-2.5 h-2.5 bg-leaf-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t-2 border-earth-100 bg-white">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  sendMessage(input);
                }}
                className="flex gap-3"
              >
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Sualınızı yazın (məs: Pomidoru nə vaxt suvarmalıyam?)..."
                  className="flex-1 px-5 py-3 bg-earth-50 border-2 border-earth-200 rounded-xl text-sm focus:outline-none focus:border-leaf-400 focus:ring-2 focus:ring-leaf-100 transition-all"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || loading}
                  className="px-6 py-3 bg-gradient-to-br from-leaf-500 to-leaf-600 text-white rounded-xl flex items-center gap-2 hover:from-leaf-600 hover:to-leaf-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      <span className="hidden sm:inline font-medium">Göndər</span>
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Info Section */}
          <div className="mt-6 card p-6 bg-gradient-to-br from-leaf-50 to-leaf-100 border-2 border-leaf-200">
            <div className="flex items-start gap-3">
              <Sparkles className="w-6 h-6 text-leaf-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-earth-800 mb-2">Məsləhətçi necə işləyir?</h3>
                <ul className="text-sm text-earth-600 space-y-1">
                  <li>✓ Suvarma, gübrələmə və zərərverici haqqında suallar verin</li>
                  <li>✓ Heyvandarlıq, yemləmə və xəstəliklər barədə məlumat alın</li>
                  <li>✓ Hava şəraiti və yığım vaxtı üzrə tövsiyələr alın</li>
                  <li>✓ Daha dəqiq tövsiyələr üçün <Link href="/recommendations" className="text-leaf-600 font-medium hover:underline">Tövsiyə Al</Link> bölməsinə keçin</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
