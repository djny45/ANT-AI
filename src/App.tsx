import Nav from './components/Nav'
import Hero from './components/Hero'
import Architecture from './components/Architecture'
import Capabilities from './components/Capabilities'
import Workflows from './components/Workflows'
import Principles from './components/Principles'
import CodeBlock from './components/CodeBlock'
import ApiKey from './components/ApiKey'
import ChatBox from './components/ChatBox'
import Roadmap from './components/Roadmap'
import CTA from './components/CTA'
import Footer from './components/Footer'

function App() {
  return (
    <div className="relative min-h-screen w-full bg-[#0a0a0a] text-white antialiased selection:bg-amber-500/30">
      <Nav />
      <main>
        <Hero />
        <Architecture />
        <Capabilities />
        <Workflows />
        <Principles />
        <CodeBlock />
        <ApiKey />
        <ChatBox />
        <Roadmap />
        <CTA />
      </main>
      <Footer />
    </div>
  )
}

export default App