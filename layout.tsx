import Link from 'next/link'
import { ReactNode } from 'react'

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <Link href="/" className="text-xl font-bold text-blue-600">
                Network Simulation System
              </Link>
            </div>
            <div className="hidden md:flex space-x-8">
              <Link href="/" className="text-gray-700 hover:text-blue-600 transition duration-300">
                Home
              </Link>
              <Link href="/features" className="text-gray-700 hover:text-blue-600 transition duration-300">
                Features
              </Link>
              <Link href="/documentation" className="text-gray-700 hover:text-blue-600 transition duration-300">
                Documentation
              </Link>
              <Link href="/github" className="text-gray-700 hover:text-blue-600 transition duration-300">
                GitHub
              </Link>
            </div>
            <div className="md:hidden">
              <button className="text-gray-700 hover:text-blue-600 focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>
        {children}
      </main>
    </div>
  )
}
