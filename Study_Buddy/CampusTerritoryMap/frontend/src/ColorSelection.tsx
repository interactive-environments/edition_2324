


type Props = {
  colors: { square: string, hexagon: string, faculty: string }[],
  selectedColor: { square: string, hexagon: string },
  setSelectedColor: React.Dispatch<React.SetStateAction<{
    square: string;
    hexagon: string;
    faculty: string;
  }>>

}
export default ({ colors, selectedColor, setSelectedColor }: Props) => {

  return (
    <>
      {
        colors.map(color => {
          return (
            <div
              className="relative w-10 h-11 overflow-hidden"
              style={{
                clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
              }}
            >
              <div
                key={color.square}
                className={`absolute inset-0 flex justify-center items-center ${color.square}`}
                onClick={() => setSelectedColor(color)}
              >
                <h1
                  className={`${selectedColor.square === color.square ? 'font-black text-black' : 'text-white'}`}
                >
                  {color.faculty}
                </h1>
              </div>
            </div>
          )
        })
      }
    </>
  )
}