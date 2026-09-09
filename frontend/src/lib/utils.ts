export const cn = (...classes: (string | boolean | undefined | null)[]) =>
  classes.filter(Boolean).join(' ')

export const formatNumber = (n: number) => {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return n.toString()
}
