
CREATE TABLE person(
   person_id INT,
   lastname VARCHAR(255) NOT NULL,
   firstname VARCHAR(255) NOT NULL,
   PRIMARY KEY(person_id)
);

CREATE TABLE teacher(
   person_id INT,
   skill VARCHAR(255),
   PRIMARY KEY(person_id),
   FOREIGN KEY(person_id) REFERENCES person(person_id)
);

CREATE TABLE address(
   number INT,
   street VARCHAR(255),
   town VARCHAR(255),
   postcode INT,
   PRIMARY KEY(number, street, town, postcode)
);

CREATE TABLE room(
   room_id VARCHAR(255),
   PRIMARY KEY(room_id)
);

CREATE TABLE subject(
   matter_id VARCHAR(255),
   PRIMARY KEY(matter_id)
);

CREATE TABLE student(
   person_id INT,
   degree VARCHAR(255),
   number INT NOT NULL,
   street VARCHAR(255) NOT NULL,
   town VARCHAR(255) NOT NULL,
   postcode INT NOT NULL,
   PRIMARY KEY(person_id),
   UNIQUE(number, street, town, postcode),
   FOREIGN KEY(person_id) REFERENCES person(person_id),
   FOREIGN KEY(number, street, town, postcode) REFERENCES address(number, street, town, postcode)
);

CREATE TABLE courses(
   room_id VARCHAR(255),
   start_at DATETIME,
   end_at DATETIME,
   matter_id VARCHAR(255) NOT NULL,
   person_id INT NOT NULL,
   person_id_1 INT NOT NULL,
   PRIMARY KEY(room_id, start_at, end_at),
   FOREIGN KEY(room_id) REFERENCES room(room_id),
   FOREIGN KEY(matter_id) REFERENCES subject(matter_id),
   FOREIGN KEY(person_id) REFERENCES student(person_id),
   FOREIGN KEY(person_id_1) REFERENCES teacher(person_id)
);