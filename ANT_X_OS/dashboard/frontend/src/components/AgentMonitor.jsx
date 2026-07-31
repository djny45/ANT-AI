export default function AgentMonitor({agents=[]}) {
  return (
    <section>
      <h2>Agents</h2>
      {agents.map((agent, index) => (
        <div key={index}>{agent}</div>
      ))}
    </section>
  );
}
