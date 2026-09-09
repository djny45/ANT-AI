import { useEffect, useRef } from 'react'

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  targetX: number
  targetY: number
  size: number
  hue: number
  alpha: number
  trail: Array<{ x: number; y: number }>
}

interface SwarmCanvasProps {
  density?: number
  interactive?: boolean
  className?: string
}

export default function SwarmCanvas({
  density = 0.00008,
  interactive = true,
  className = '',
}: SwarmCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const particlesRef = useRef<Particle[]>([])
  const mouseRef = useRef({ x: -1000, y: -1000, active: false })
  const rafRef = useRef<number>(0)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = Math.min(window.devicePixelRatio || 1, 2)

    const resize = () => {
      const rect = canvas.getBoundingClientRect()
      canvas.width = rect.width * dpr
      canvas.height = rect.height * dpr
      ctx.scale(dpr, dpr)

      // Re-seed particles
      const count = Math.floor(rect.width * rect.height * density)
      const particles: Particle[] = []
      for (let i = 0; i < count; i++) {
        particles.push(createParticle(rect.width, rect.height, i))
      }
      particlesRef.current = particles
    }

    const createParticle = (
      w: number,
      h: number,
      i: number,
    ): Particle => {
      const angle = Math.random() * Math.PI * 2
      const radius = Math.random() * Math.min(w, h) * 0.45
      const cx = w / 2
      const cy = h / 2
      return {
        x: cx + Math.cos(angle) * radius,
        y: cy + Math.sin(angle) * radius,
        vx: (Math.random() - 0.5) * 0.2,
        vy: (Math.random() - 0.5) * 0.2,
        targetX: cx,
        targetY: cy,
        size: Math.random() * 1.6 + 0.4,
        hue: 32 + Math.random() * 18, // amber range
        alpha: Math.random() * 0.5 + 0.3,
        trail: [],
      }
    }

    const onMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect()
      mouseRef.current.x = e.clientX - rect.left
      mouseRef.current.y = e.clientY - rect.top
      mouseRef.current.active = true
    }

    const onLeave = () => {
      mouseRef.current.active = false
      mouseRef.current.x = -1000
      mouseRef.current.y = -1000
    }

    const onTouch = (e: TouchEvent) => {
      const rect = canvas.getBoundingClientRect()
      const t = e.touches[0]
      if (t) {
        mouseRef.current.x = t.clientX - rect.left
        mouseRef.current.y = t.clientY - rect.top
        mouseRef.current.active = true
      }
    }

    const draw = () => {
      const w = canvas.width / dpr
      const h = canvas.height / dpr
      ctx.clearRect(0, 0, w, h)

      const particles = particlesRef.current
      const mouse = mouseRef.current

      // Update & draw each particle
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i]

        // Mouse attraction/repulsion
        if (mouse.active) {
          const dx = mouse.x - p.x
          const dy = mouse.y - p.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          const radius = 180
          if (dist < radius && dist > 0) {
            const force = (1 - dist / radius) * 0.35
            // Orbit behavior: perpendicular component + attraction
            const angle = Math.atan2(dy, dx)
            p.vx += Math.cos(angle + Math.PI / 2) * force * 0.6
            p.vy += Math.sin(angle + Math.PI / 2) * force * 0.6
            // Slight pull toward cursor
            p.vx += (dx / dist) * force * 0.15
            p.vy += (dy / dist) * force * 0.15
          }
        }

        // Gentle drift toward center (colony pulse)
        const cx = w / 2
        const cy = h / 2
        const toCx = cx - p.x
        const toCy = cy - p.y
        const toCenterDist = Math.sqrt(toCx * toCx + toCy * toCy)
        if (toCenterDist > 50) {
          p.vx += (toCx / toCenterDist) * 0.005
          p.vy += (toCy / toCenterDist) * 0.005
        }

        // Random jitter (ant foraging)
        p.vx += (Math.random() - 0.5) * 0.05
        p.vy += (Math.random() - 0.5) * 0.05

        // Apply velocity with damping
        p.vx *= 0.96
        p.vy *= 0.96
        // Speed cap
        const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy)
        if (speed > 3) {
          p.vx = (p.vx / speed) * 3
          p.vy = (p.vy / speed) * 3
        }
        p.x += p.vx
        p.y += p.vy

        // Wrap
        if (p.x < 0) p.x = w
        if (p.x > w) p.x = 0
        if (p.y < 0) p.y = h
        if (p.y > h) p.y = 0

        // Trail
        p.trail.push({ x: p.x, y: p.y })
        if (p.trail.length > 6) p.trail.shift()

        // Draw trail
        if (p.trail.length > 1) {
          ctx.beginPath()
          ctx.moveTo(p.trail[0].x, p.trail[0].y)
          for (let j = 1; j < p.trail.length; j++) {
            ctx.lineTo(p.trail[j].x, p.trail[j].y)
          }
          ctx.strokeStyle = `hsla(${p.hue}, 90%, 60%, ${p.alpha * 0.15})`
          ctx.lineWidth = p.size * 0.6
          ctx.stroke()
        }

        // Draw particle
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
        ctx.fillStyle = `hsla(${p.hue}, 95%, 65%, ${p.alpha})`
        ctx.fill()

        // Glow
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size * 2.5, 0, Math.PI * 2)
        ctx.fillStyle = `hsla(${p.hue}, 95%, 65%, ${p.alpha * 0.1})`
        ctx.fill()
      }

      // Draw connections between nearby particles (pheromone trails)
      const maxDist = 80
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const a = particles[i]
          const b = particles[j]
          const dx = a.x - b.x
          const dy = a.y - b.y
          const d = Math.sqrt(dx * dx + dy * dy)
          if (d < maxDist) {
            const alpha = (1 - d / maxDist) * 0.08
            ctx.beginPath()
            ctx.moveTo(a.x, a.y)
            ctx.lineTo(b.x, b.y)
            ctx.strokeStyle = `hsla(38, 90%, 60%, ${alpha})`
            ctx.lineWidth = 0.6
            ctx.stroke()
          }
        }
      }

      // Mouse glow
      if (mouse.active) {
        const grad = ctx.createRadialGradient(
          mouse.x,
          mouse.y,
          0,
          mouse.x,
          mouse.y,
          140,
        )
        grad.addColorStop(0, 'rgba(245, 158, 11, 0.12)')
        grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.04)')
        grad.addColorStop(1, 'rgba(245, 158, 11, 0)')
        ctx.fillStyle = grad
        ctx.fillRect(0, 0, w, h)
      }

      rafRef.current = requestAnimationFrame(draw)
    }

    resize()
    rafRef.current = requestAnimationFrame(draw)

    if (interactive) {
      window.addEventListener('mousemove', onMove)
      window.addEventListener('mouseleave', onLeave)
      window.addEventListener('touchmove', onTouch)
    }
    window.addEventListener('resize', resize)

    return () => {
      cancelAnimationFrame(rafRef.current)
      window.removeEventListener('mousemove', onMove)
      window.removeEventListener('mouseleave', onLeave)
      window.removeEventListener('touchmove', onTouch)
      window.removeEventListener('resize', resize)
    }
  }, [density, interactive])

  return (
    <canvas
      ref={canvasRef}
      className={`pointer-events-none absolute inset-0 h-full w-full ${className}`}
    />
  )
}