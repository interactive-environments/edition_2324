import { HexGrid, Layout } from 'react-hexgrid';
import HexagonComponent from './Hexagon';
import { Hexagon } from './App';
import windowHook from './hooks/windowHook';

type Props = {
  selectedColor: string,
  grid: Hexagon[],
  canUserPlaceHexagon: boolean,
  isMobile: boolean
}

export default ({ selectedColor, grid, canUserPlaceHexagon, isMobile }: Props) => {

  const { width, height } = windowHook();
  
  return (
    <div className='h-4/5'> 
      {
        isMobile
          ?
          <HexGrid width={width} height={height * .85} viewBox="-50 -50 100 100">
            <Layout size={{ x: 2, y: 2 }} flat={true} spacing={1.1} origin={{ x: 0, y: -16 }}>
              {
                grid.map((hexagon, index) =>
                  <HexagonComponent
                    hexagon={hexagon}
                    canUserPlaceHexagon={canUserPlaceHexagon}
                    grid={grid}
                    selectedColor={selectedColor}
                    key={index}
                  />
                )
              }
            </Layout>
          </HexGrid>
          :
          <HexGrid width={width} height={height * .85} viewBox="-50 -50 100 100">
            <Layout size={{ x: 2.5, y: 2.5 }} flat={true} spacing={1.1} origin={{ x: 0, y: 0 }}>
              {
                grid.map((hexagon, index) =>
                  <HexagonComponent
                    hexagon={hexagon}
                    canUserPlaceHexagon={canUserPlaceHexagon}
                    grid={grid}
                    selectedColor={selectedColor}
                    key={index}
                  />
                )
              }
            </Layout>
          </HexGrid>
      }
    </div>
  )
}