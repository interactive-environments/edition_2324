export type HexagonCoordinates = { q: number; s: number; r: number };

export const generateHexagonGrid = (radius: number): HexagonCoordinates[] => {

  const hexagonGrid: HexagonCoordinates[] = [];

  for (let q = -radius; q <= radius; q++) {
    const minS = Math.max(-radius, -q - radius);
    const maxS = Math.min(radius, -q + radius);

    for (let s = minS; s <= maxS; s++) {
      const r = -q - s;
      hexagonGrid.push({ q, s, r });
    }
  }

  return hexagonGrid;
}