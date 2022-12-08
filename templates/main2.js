// const studentsData = [
//   {
//     firstName: 'Василий',
//     lastName: 'Петров',
//     admissionYear: 2019,
//     courseName: 'Java',
//   },
//   {
//     firstName: 'Иван',
//     lastName: 'Иванов',
//     admissionYear: 2018,
//     courseName: 'JavaScript',
//   },
//   {
//     firstName: 'Александр',
//     lastName: 'Федоров',
//     admissionYear: 2017,
//     courseName: 'Python',
//   },
//   {
//     firstName: 'Николай',
//     lastName: 'Петров',
//     admissionYear: 2019,
//     courseName: 'Android',
//   },
// ];


  
//   class User {
//     constructor({ firstName, lastName }) {
//       this.firstName = firstName;
//       this.lastName = lastName;
//     }
  
//     get fullName() {
//       return `${this.firstName} ${this.lastName}`;
//     }
//   }

//   class Student extends User {
//     constructor({ admissionYear, courseName, firstName, lastName }) {
//       super({ firstName, lastName });
//       this.admissionYear = admissionYear;
//       this.courseName = courseName;
//     }
  
//     get course() {
//       const now = new Date();
//       return now.getFullYear() - this.admissionYear;
//     }
//   }

//   class Students {
//     constructor(studentsData) {
//       this.studentsData = studentsData.map(
//         (prop) =>
//           new Student({
//             admissionYear: prop.admissionYear,
//             courseName: prop.courseName,
//             firstName: prop.firstName,
//             lastName: prop.lastName,
//           }),
//       );
//     }
  
//     getInfo() {
//       const result = [];
//       function byField(field) {
//         return (a, b) => (a[field] < b[field] ? 1 : -1);
//       }
//       this.studentsData.sort(byField('admissionYear'));
//       for (let i = 0; i < this.studentsData.length; i++) {
//         result.push(
//           `${this.studentsData[i].fullName} - ${this.studentsData[i].courseName}, ${this.studentsData[i].course} курс`,
//         );
//       }
//       return result;
//     }
//   }

//   const std1 = new Students(studentsData);
// console.log(std1.getInfo());  