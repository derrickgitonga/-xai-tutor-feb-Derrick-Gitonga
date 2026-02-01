'use client';

import { useTheme } from '../../context/ThemeContext';

export default function Header() {
  const { theme, toggleTheme } = useTheme();
  return (
    <header className="h-16 bg-gray-50 border-b border-gray-200 flex items-center justify-between px-6">
      {/* Left Section */}
      <div className="flex items-center">
        {/* Page Title */}
        <h1 className="text-xl font-semibold text-gray-800">Orders</h1>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        {/* User Avatars */}
        <div className="flex items-center">
          <div className="flex -space-x-2">
            <img
              src="https://ui-avatars.com/api/?name=User+1&background=f97316&color=fff&size=32"
              alt="User 1"
              className="w-8 h-8 rounded-full border-2 border-white"
            />
            <img
              src="https://ui-avatars.com/api/?name=User+2&background=3b82f6&color=fff&size=32"
              alt="User 2"
              className="w-8 h-8 rounded-full border-2 border-white"
            />
          </div>
          <span className="ml-2 px-2 py-0.5 text-sm text-purple-600 bg-purple-100 rounded-full">+2</span>
          <button className="ml-2 w-8 h-8 rounded-full border-2 border-dashed border-gray-400 bg-transparent flex items-center justify-center text-gray-400 hover:border-gray-500 hover:text-gray-500">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>

        {/* Dark Mode Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
          aria-label="Toggle dark mode"
        >
          {theme === 'light' ? (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          )}
        </button>

        {/* Notification Bell */}
        <button className="relative p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-medium rounded-full flex items-center justify-center">
            24
          </span>
        </button>

        {/* Search Bar */}
        <div className="relative">
          <div className="flex items-center gap-2 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg w-64">
            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search anything"
              className="flex-1 bg-transparent text-sm text-gray-600 placeholder-gray-400 focus:outline-none"
            />
            <kbd className="px-1.5 py-0.5 text-xs text-gray-400 bg-white border border-gray-200 rounded">
              ⌘K
            </kbd>
          </div>
        </div>

        {/* Profile Avatar */}
        <button className="relative">
          <img
            src="https://ui-avatars.com/api/?name=John+Doe&background=e5e7eb&color=374151&size=40"
            alt="Profile"
            className="w-10 h-10 rounded-full"
          />
          <svg className="absolute -bottom-0.5 -right-0.5 w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </header>
  );
}
