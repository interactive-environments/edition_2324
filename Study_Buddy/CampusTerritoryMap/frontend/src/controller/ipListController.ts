import { IPList } from "../App";

export const isIPInList = (ip: string, ipList: IPList) => {

  const userIndex = ipList.findIndex(user => user.ip === ip);

  return userIndex !== -1;
}

export const hasEnoughTimePassed = (ip: string, ipList: IPList, minutes: number) => {

  const userIndex = ipList.findIndex(user => user.ip === ip);
  const lastUpdate = ipList[userIndex].timestamp;

  const diffInMilliseconds = Math.abs(new Date(lastUpdate).getTime() - new Date().getTime());
  const minutesDifference = diffInMilliseconds / (1000 * 60); // 1000 milliseconds in a second, 60 seconds in a minute

  return minutesDifference > minutes;
}