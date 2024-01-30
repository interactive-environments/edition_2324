import windowHook from './hooks/windowHook';

type Props = {
  radius: number
}

export default ({ radius }: Props) => {

  const facultiesAndColors = [
    { faculty: 'TPM', color: 'bg-purple-600' },
    { faculty: '3ME', color: 'bg-red-600' },
    { faculty: 'IO', color: 'bg-indigo-600' },
    { faculty: 'TNW', color: 'bg-yellow-600' },
    { faculty: 'LR', color: 'bg-orange-600' },
    { faculty: 'CiTG', color: 'bg-sky-600' },
    { faculty: 'BK', color: 'bg-green-600' },
    { faculty: 'EWI', color: 'bg-pink-600' },
  ];
  const { width, height } = windowHook();

  const calculatePosition = (index: number, totalItems: number) => {
    const angle = (Math.PI * 2) / totalItems;
    const centerX = width / 2; 
    const centerY = height / 2;
    const shiftAngle = angle / 2;

    const x = Math.round(centerX + radius * Math.cos(shiftAngle + index * angle));
    const y = Math.round(centerY + radius * Math.sin(shiftAngle + index * angle));


    return { x, y };
  };

  return (
    <div className="justify-center items-center">
      {facultiesAndColors.map(({ faculty, color }, index) => {
        const position = calculatePosition(index, facultiesAndColors.length);
        return (
          <div
            key={index}
            className={"absolute transform p-1 -translate-x-1/2 -translate-y-1/2 " + color} 
            style={{ left: position.x, top: position.y }}
          >
            <span className="text-sm md:text-2xl">{faculty}</span>
          </div>
        );
      })}
    </div>
  );
}