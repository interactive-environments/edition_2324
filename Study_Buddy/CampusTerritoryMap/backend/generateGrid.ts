import fs from 'fs';
import { resetIPList } from './ipController';

type HexagonCoordinates = { 
  coordinates: { q: number; s: number; r: number },
  color: string,
  index: number,
  neighbors: number[]
};

const FILE_PATH = 'data.json';

const radius = process.argv[2];

let colorIndex = 0;
const initialColorsArray = [
  'fill-red-600',
  'fill-blue-600',
  'fill-green-600',
  'fill-yellow-600',
  'fill-pink-600',
  'fill-purple-600',
  'fill-sky-600',
  'fill-indigo-600'
];

/**
 * Error handling
 */

//? Radius not provided
if (!radius) 
  throw Error('No argument provided for the radius')

const parsedRadius = parseInt(radius, 10);

//? Invalid radius
if (isNaN(parsedRadius) || parsedRadius <= 0 || parsedRadius > 10) 
  throw Error(`Invalid radius provided: ${radius}`)


// --------------------------------------------------------------------

/**
 * Generate grid
 */
const generateHexagonGrid = (radius: number): HexagonCoordinates[] => {
  const hexagonGrid: HexagonCoordinates[] = [];

  for (let q = -radius; q <= radius; q++) {
    const minS = Math.max(-radius, -q - radius);
    const maxS = Math.min(radius, -q + radius);

    for (let s = minS; s <= maxS; s++) {
      const r = -q - s;

      const currentHexagon: HexagonCoordinates = {
        coordinates: { q, s, r },
        color: 'fill-stone-600', // Assign a color to edge hexagons
        index: hexagonGrid.length,
        neighbors: [] // Initialize an empty array for storing neighbor indices
      };

      hexagonGrid.push(currentHexagon);
    }
  }

  // Helper function to get the index of a hexagon in the grid
  const getHexagonIndex = (q: number, s: number, r: number): number | undefined => {
    const foundHexagon = hexagonGrid.find(
      hexagon => hexagon.coordinates.q === q && hexagon.coordinates.s === s && hexagon.coordinates.r === r
    );
    return foundHexagon ? foundHexagon.index : undefined;
  };

  // Coordinates of corner hexagons
  const cornerCoordinates = [
    { q: radius, s: -radius, r: 0 },
    { q: -radius, s: radius, r: 0 },
    { q: 0, s: -radius, r: radius },
    { q: 0, s: radius, r: -radius },
    { q: -radius, s: 0, r: radius },
    { q: radius, s: 0, r: -radius }
  ];

  // Color the corner hexagons
  cornerCoordinates.forEach(({ q, s, r }) => {
    const cornerHexagonIndex = getHexagonIndex(q, s, r);
    if (cornerHexagonIndex !== undefined) {
      hexagonGrid[cornerHexagonIndex].color = initialColorsArray[colorIndex];
      colorIndex++;
    }
  });

  // Calculate and assign indices of neighboring hexagons
  hexagonGrid.forEach(hexagon => {
    const { q, s, r } = hexagon.coordinates;

    // Offsets for neighboring hexagons in axial coordinates
    const neighborOffsets = [
      [1, 0, -1], [1, -1, 0], [0, -1, 1],
      [-1, 0, 1], [-1, 1, 0], [0, 1, -1]
    ];

    for (const [dq, ds, dr] of neighborOffsets) {
      const neighborQ = q + dq;
      const neighborS = s + ds;
      const neighborR = r + dr;

      const neighborIndex = getHexagonIndex(neighborQ, neighborS, neighborR);
      if (neighborIndex !== undefined) {
        hexagon.neighbors.push(neighborIndex);
      }
    }
  });

  return hexagonGrid;
};


/* function generateHexagonGrid(sideLength: number): HexagonCoordinates[] {

  const rows = sideLength;
  const cols = sideLength;
  const hexagons: HexagonCoordinates[] = [];
  let index = 0;

  for (let r = 0; r < rows; r++) {
    const offset = Math.floor(r / 2);
    for (let q = -offset; q < cols - offset; q++) {
      const hexagon: HexagonCoordinates = {
        coordinates: { q, s: -q - r, r },
        color: 'fill-stone-300',
        index,
        neighbors: []
      };

      hexagons.push(hexagon);
      index++;
    }
  }

  const directions = [
    [1, 0, -1],
    [1, -1, 0],
    [0, -1, 1],
    [-1, 0, 1],
    [-1, 1, 0],
    [0, 1, -1]
  ];

  for (let i = 0; i < hexagons.length; i++) {
    const { q, r } = hexagons[i].coordinates;

    for (const [dq, dr, ds] of directions) {
      const neighborQ = q + dq;
      const neighborR = r + dr;
      const neighborS = -neighborQ - neighborR;

      const neighbor = hexagons.find(
        hex =>
          hex.coordinates.q === neighborQ &&
          hex.coordinates.r === neighborR &&
          hex.coordinates.s === neighborS
      );

      if (neighbor) {
        hexagons[i].neighbors.push(neighbor.index);
      }
    }
  }

  return hexagons;
}

 */
/**
 * Write grid to file
 */
const writeToFile = (filePath: string, data: string) => {
  fs.writeFile(filePath, data, 'utf8', (err) => {
    if (err) {
      console.error('Error writing file:', err);
    } else {
      console.log('File updated successfully');
    }
  });
}

const grid = generateHexagonGrid(parsedRadius);
const stringGrid = JSON.stringify(grid, null, 2);

resetIPList();
writeToFile(FILE_PATH, stringGrid);