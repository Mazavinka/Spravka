const users = new Map([
    [1, {
        id: 1,
        name: 'ivan',
        lastname:'ivanov',  
    }],
    [2, {
        id: 2,
        name: 'nikit',
        lastname:'nikitov',  
    }],
    [3, {
        id: 3,
        name: 'povar',
        lastname:'povarov',  
    }]
]);

const usersMap = users.reduce(((acc,user) => {
    acc.set(user.id,user);
    return acc;
},new Map())); 


console.log(users);
console.log(Array.from(usersMap.values()));
