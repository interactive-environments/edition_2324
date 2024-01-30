import * as fs from 'fs';

interface IPData {
  users: { ip: string, timestamp: Date }[];
}

const FILE_PATH = 'IP_list.json';

export const updateOrGenerateTimeStamp = (ip: string) => {
  try {
    // Read the content of the file
    const data: IPData = JSON.parse(fs.readFileSync(FILE_PATH, 'utf8'));
    const timestamp = new Date();

    const userIndex = data.users.findIndex(user => user.ip === ip);

    // User is not in the list, add entry
    if (userIndex === -1)
      data.users.push({ 'ip': ip, 'timestamp': timestamp });
    else  //User is in the list, update timestamp
      data.users[userIndex].timestamp = timestamp;

    // Write the updated data back to the file
    fs.writeFileSync(FILE_PATH, JSON.stringify(data, null, 2), 'utf8');

    return data.users;

  } catch (error) {
    console.error('Error:', error);
  }
};

export const getIPList = () => {

  const data: Buffer = fs.readFileSync(FILE_PATH);
  const fileContent: string = data.toString();

  return JSON.parse(fileContent).users;
}

export const resetIPList = () => {

  const data = {
    "users": [{}]
  }
  
  fs.writeFileSync(FILE_PATH, JSON.stringify(data, null, 2), 'utf8');

}