import * as fs from 'fs';

const FILE_PATH = 'map.json';

export const retrieveGrid = () => {

  const data: Buffer = fs.readFileSync(FILE_PATH);
  const fileContent: string = data.toString();

  return JSON.parse(fileContent);
}

export const updateColor = (newColor: string, index: number) => {

  const startTime = performance.now()

  const jsonData = JSON.parse(fs.readFileSync(FILE_PATH, 'utf-8'));

  jsonData[index].color = newColor;

  fs.writeFileSync(FILE_PATH, JSON.stringify(jsonData, null, 2));

  const endTime = performance.now();
  
  //console.log(`Time taken to complete operation: ${endTime - startTime} ms`);

  return jsonData;
}