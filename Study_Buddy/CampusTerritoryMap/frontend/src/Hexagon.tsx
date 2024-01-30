import { useContext, useState } from "react";
import { Hexagon } from "react-hexgrid";
import { Hexagon as HexagonType, SocketContext } from "./App";

type Props = {
  hexagon: HexagonType,
  grid: HexagonType[],
  selectedColor: string,
  canUserPlaceHexagon: boolean
}

const BLANK_HEXAGON_COLOR = "fill-stone-700";

export default ({ hexagon, grid, selectedColor, canUserPlaceHexagon }: Props) => {

  const socket = useContext(SocketContext);

  const { q, r, s } = hexagon.coordinates;
  const hexagonColor = hexagon.color;
  const index = hexagon.index
  
  const neighborsColors = hexagon.neighbors.map(i => grid[i].color);

  const [displayNewColor, setDisplayNewColor] = useState(false);
  const [displayGray, setDisplayGray] = useState(false);

  const changeColor = () => {

    console.log(q,r,s);

    if (canUserPlaceHexagon
      && neighborsColors.includes(selectedColor)
      && hexagonColor === BLANK_HEXAGON_COLOR
    )
      socket.emit('hexelPlaced', selectedColor, index);
  }

  const hoverController = () => {
    if (neighborsColors.includes(selectedColor) && hexagonColor === BLANK_HEXAGON_COLOR)
      setDisplayNewColor(true);
    else if (hexagonColor !== selectedColor)
      setDisplayGray(true);

  }

  return (
    <Hexagon
      q={q} r={r} s={s}
      className={ displayNewColor ? selectedColor : displayGray ? 'fill-stone-500' : hexagonColor }
      onMouseEnter={() => hoverController()}
      onMouseLeave={() => { 
        setDisplayGray(false);
        setDisplayNewColor(false);
      }}
      onClick={changeColor}
    />
  )
}