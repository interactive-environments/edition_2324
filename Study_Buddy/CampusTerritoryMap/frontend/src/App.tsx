import io from 'socket.io-client';
import { createContext, useEffect, useState } from 'react'
import loading from './assets/loading.svg';
import { SERVER_URL } from '../util.json';
import Map from './Map';
import windowHook from './hooks/windowHook';
import Words from './Words';
import ColorSelection from './ColorSelection';
import { hasEnoughTimePassed, isIPInList } from './controller/ipListController';

export type Hexagon = { 
  coordinates: {q: number, r: number, s: number }, 
  color: string,
  index: number,
  neighbors: number[]
}

export type IPList = { 'ip': string, 'timestamp': Date }[]

const socket = io(SERVER_URL); // Replace with your server URL

const colors = [
  { square: 'bg-red-600', hexagon: 'fill-red-600', faculty: '3ME' },
  //{square: 'bg-blue-600', hexagon: 'fill-blue-600'},
  { square: 'bg-green-600', hexagon: 'fill-green-600', faculty: 'BK' },
  { square: 'bg-yellow-600', hexagon: 'fill-yellow-600', faculty: 'TNW' },
  { square: 'bg-pink-600', hexagon: 'fill-pink-600', faculty: 'EWI' },
  { square: 'bg-purple-600', hexagon: 'fill-purple-600', faculty: 'TPM' },
  { square: 'bg-indigo-600', hexagon: 'fill-indigo-600', faculty: 'IO' },
  { square: 'bg-sky-600', hexagon: 'fill-sky-600', faculty: 'CiTG' },
  { square: 'bg-orange-600', hexagon: 'fill-orange-600', faculty: 'LR' },
];

export const SocketContext = createContext(socket);
const MINUTES_WINDOW = 5;

//TODO Fix when trying to add a hexagon on one that has a different color, it shouldn't color it

function App() {

  const [grid, setGrid] = useState<Hexagon[]>();
  const [IPList, setIPList] = useState<IPList>();
  const [localIP, setLocalIP] = useState<string>('');
  const [selectedColor, setSelectedColor] = useState(colors[0]);
  const [canUserPlaceHexagon, setCanUserPlaceHexagon] = useState(true);

  const { width } = windowHook();

  useEffect(() => {

    socket.on('IP', (IP) => setLocalIP(IP));

    socket.on('grid', (stringifiedGrid) => {
      const parsedGrid = JSON.parse(stringifiedGrid);
      setGrid(parsedGrid);
    });

    socket.on('IPList', (stringifiedIPList, IP) => {

      const parsedList = JSON.parse(stringifiedIPList);
      setIPList(parsedList);

      const userNotInListOrEnoughTimePassed = !isIPInList(IP, parsedList) || hasEnoughTimePassed(IP, parsedList, MINUTES_WINDOW);
      setCanUserPlaceHexagon(userNotInListOrEnoughTimePassed);
    })
  })

  const isMobile = width < 1000;

  //bg-hex_svg
  return (
    <SocketContext.Provider value={socket}>
      <div className='h-screen w-screen m-0 p-0 flex flex-col justify-start items-center bg-stone-300  bg-center bg-no-repeat bg-cover'>
        {
          grid && IPList && localIP
            ?
            <>
              <div className='flex flex-col justify-center items-center'>

                {
                  isMobile
                    ?
                    <>
                      <h1 className='text-black mx-8 text-center font-bold'>
                        Select your faculty color and then place a hexagon next to an existing one
                      </h1>
                      <h1 className='text-black mx-8 text-center font-medium mt-8'>
                        Points: {canUserPlaceHexagon ? 5 : 0}
                      </h1>
                    </>
                    : ''
                }
                <Words radius={isMobile ? 190 : 460} />
                <Map
                  selectedColor={selectedColor.hexagon}
                  canUserPlaceHexagon={canUserPlaceHexagon}
                  grid={grid}
                  isMobile={isMobile}
                />
                {
                  isMobile
                    ?
                    canUserPlaceHexagon
                      ?
                      <div className='absolute bottom-5 w-3/4 grid grid-cols-4 items-center justify-center gap-4'>
                        <ColorSelection
                          colors={colors}
                          selectedColor={selectedColor}
                          setSelectedColor={setSelectedColor}
                        />
                      </div>
                      :

                      <div className='absolute bottom-5 w-3/4  items-center justify-center '>
                        <h1 className='text-black mx-8 text-center font-medium'>
                          You don't have enough points to place a hexagon
                        </h1>
                      </div>
                    :
                    <></>
                }
              </div>
            </>
            :
            <div className='flex justify-center items-center'>
              <img src={loading} className='w-48 h-48' />
            </div>
        }
      </div>
    </SocketContext.Provider>
  )
}

export default App
