import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="container mx-auto px-6 py-16">
          <div className="flex flex-col items-center">
            <h1 className="text-4xl md:text-5xl font-bold text-center mb-6">
              Network Simulation with Attack Detection & ML Prediction
            </h1>
            <p className="text-xl text-center max-w-3xl mb-8">
              A comprehensive platform for simulating network attacks, implementing defense mechanisms, 
              and using machine learning to predict and evaluate attack blocking accuracy.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/features" className="bg-white text-blue-700 hover:bg-blue-50 font-semibold py-3 px-6 rounded-lg transition duration-300">
                Explore Features
              </Link>
              <Link href="/documentation" className="bg-transparent hover:bg-blue-500 text-white border border-white font-semibold py-3 px-6 rounded-lg transition duration-300">
                View Documentation
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Main Features */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Key Components</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Network Topology */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Network Topology</h3>
              <p className="text-gray-600 mb-4">
                Virtual network environment with legitimate clients, attackers, a target server, and a firewall/IDS node.
              </p>
              <Link href="/components/topology" className="text-blue-600 hover:text-blue-800 font-medium">
                Learn more →
              </Link>
            </div>

            {/* Attack Simulation */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="h-12 w-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Attack Simulation</h3>
              <p className="text-gray-600 mb-4">
                Generates various network attacks including DoS, port scanning, SYN flood, and more with configurable parameters.
              </p>
              <Link href="/components/attacks" className="text-blue-600 hover:text-blue-800 font-medium">
                Learn more →
              </Link>
            </div>

            {/* Defense Mechanisms */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Defense Mechanisms</h3>
              <p className="text-gray-600 mb-4">
                Implements traffic analysis, attack detection, and IP blocking capabilities to protect against various attacks.
              </p>
              <Link href="/components/defense" className="text-blue-600 hover:text-blue-800 font-medium">
                Learn more →
              </Link>
            </div>

            {/* Machine Learning */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Machine Learning Model</h3>
              <p className="text-gray-600 mb-4">
                Predicts attacks based on network traffic patterns and provides detailed accuracy metrics.
              </p>
              <Link href="/components/ml-model" className="text-blue-600 hover:text-blue-800 font-medium">
                Learn more →
              </Link>
            </div>

            {/* Integration */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="h-12 w-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Integrated System</h3>
              <p className="text-gray-600 mb-4">
                Connects all components into a cohesive solution for a complete network security simulation environment.
              </p>
              <Link href="/components/integration" className="text-blue-600 hover:text-blue-800 font-medium">
                Learn more →
              </Link>
            </div>

            {/* Performance Evaluation */}
            <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition duration-300">
              <div className="h-12 w-12 bg-cyan-100 rounded-lg flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-3">Performance Evaluation</h3>
              <p className="text-gray-600 mb-4">
                Evaluates system effectiveness across different attack scenarios with detailed metrics and visualizations.
              </p>
              <Link href="/components/evaluation" className="text-blue-600 hover:text-blue-800 font-medium">
                Learn more →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gray-100">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="max-w-4xl mx-auto">
            <div className="flex flex-col space-y-8">
              <div className="flex flex-col md:flex-row items-center">
                <div className="md:w-1/3 flex justify-center mb-6 md:mb-0">
                  <div className="h-16 w-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">1</div>
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-xl font-semibold mb-2">Network Setup</h3>
                  <p className="text-gray-600">
                    The system creates a virtual network topology with legitimate clients, attackers, a target server, and a firewall/IDS node using Mininet.
                  </p>
                </div>
              </div>
              
              <div className="flex flex-col md:flex-row items-center">
                <div className="md:w-1/3 flex justify-center mb-6 md:mb-0">
                  <div className="h-16 w-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">2</div>
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-xl font-semibold mb-2">Attack Generation</h3>
                  <p className="text-gray-600">
                    Attackers generate various types of network attacks with configurable parameters like duration and intensity.
                  </p>
                </div>
              </div>
              
              <div className="flex flex-col md:flex-row items-center">
                <div className="md:w-1/3 flex justify-center mb-6 md:mb-0">
                  <div className="h-16 w-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">3</div>
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-xl font-semibold mb-2">Traffic Analysis</h3>
                  <p className="text-gray-600">
                    The defense system analyzes network traffic, establishes baseline patterns, and detects anomalies that could indicate attacks.
                  </p>
                </div>
              </div>
              
              <div className="flex flex-col md:flex-row items-center">
                <div className="md:w-1/3 flex justify-center mb-6 md:mb-0">
                  <div className="h-16 w-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">4</div>
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-xl font-semibold mb-2">ML Prediction</h3>
                  <p className="text-gray-600">
                    The machine learning model predicts attacks based on extracted features from network traffic and provides confidence scores.
                  </p>
                </div>
              </div>
              
              <div className="flex flex-col md:flex-row items-center">
                <div className="md:w-1/3 flex justify-center mb-6 md:mb-0">
                  <div className="h-16 w-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">5</div>
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-xl font-semibold mb-2">Attack Mitigation</h3>
                  <p className="text-gray-600">
                    The firewall blocks malicious IP addresses based on detection results, protecting the target server from attacks.
                  </p>
                </div>
              </div>
              
              <div className="flex flex-col md:flex-row items-center">
                <div className="md:w-1/3 flex justify-center mb-6 md:mb-0">
                  <div className="h-16 w-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold">6</div>
                </div>
                <div className="md:w-2/3">
                  <h3 className="text-xl font-semibold mb-2">Performance Analysis</h3>
                  <p className="text-gray-600">
                    The system evaluates detection rates, blocking rates, and ML model accuracy across different attack scenarios.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Get Started */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
            <div className="md:flex">
              <div className="p-8 md:p-12">
                <h2 className="text-3xl font-bold text-gray-800 mb-4">Ready to Get Started?</h2>
                <p className="text-gray-600 mb-6">
                  Explore our comprehensive documentation to learn how to set up and use the network simulation system.
                </p>
                <div className="flex flex-wrap gap-4">
                  <Link href="/documentation" className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-300">
                    View Documentation
                  </Link>
                  <Link href="/github" className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-6 rounded-lg transition duration-300">
                    GitHub Repository
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between">
            <div className="mb-6 md:mb-0">
              <h3 className="text-xl font-bold mb-4">Network Simulation System</h3>
              <p className="text-gray-400 max-w-md">
                A comprehensive platform for simulating network attacks, implementing defense mechanisms, 
                and using machine learning to predict and evaluate attack blocking accuracy.
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li><Link href="/features" className="text-gray-400 hover:text-white transition duration-300">Features</Link></li>
                <li><Link href="/documentation" className="text-gray-400 hover:text-white transition duration-300">Documentation</Link></li>
                <li><Link href="/github" className="text-gray-400 hover:text-white transition duration-300">GitHub</Link></li>
                <li><Link href="/contact" className="text-gray-400 hover:text-white transition duration-300">Contact</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>© {new Date().getFullYear()} Network Simulation System. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
