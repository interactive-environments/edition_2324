import * as fs from 'fs'

const FILE_PATH = 'map.json';
const COPY_PATH = 'map_copy.json'


const reset = () => {
  try {
    const data = JSON.parse(fs.readFileSync(COPY_PATH, 'utf8'));
    fs.writeFileSync(FILE_PATH, JSON.stringify(data, null, 2), 'utf8');
  } catch (e) {
    console.log(e);
  }
}

reset();