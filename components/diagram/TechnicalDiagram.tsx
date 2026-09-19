const nodes = ["Input", "Context", "Resolve", "Execute"];

export function TechnicalDiagram() {
  return <figure className="technical-diagram"><svg viewBox="0 0 640 150" role="img" aria-labelledby="diagram-title diagram-description"><title id="diagram-title">Illustrative system continuity diagram</title><desc id="diagram-description">Four labeled nodes connected in sequence. This is a generic placeholder, not a product architecture claim.</desc>{nodes.map((node, index) => <g key={node}><rect className={index === 2 ? "diagram-node diagram-node-active" : "diagram-node"} x={index * 155 + 12} y="45" width="110" height="58" rx="8" /><text className="diagram-label" x={index * 155 + 67} y="79" textAnchor="middle">{node}</text>{index < nodes.length - 1 ? <path className="diagram-edge" d={`M${index * 155 + 122} 74 H${index * 155 + 155}`} /> : null}</g>)}</svg><figcaption>Illustrative continuity story; generic geometry remains replaceable.</figcaption></figure>;
}
