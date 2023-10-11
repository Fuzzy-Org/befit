CREATE TABLE if not exists Cardio (
	Stage int not null,
    Body int not null,
    Sex int not null,
    Sessions int,
    Time varchar(255),
    primary key (Stage, Body, Sex)
);
 
INSERT INTO Cardio VALUES (0, 2, 0, 3, '12, 15, 12 mins'),
					      (1, 2, 0, 4, '22, 25, 22, 25 mins'),
					      (0, 3, 0, 3, '15, 20, 15 mins'),
					      (1, 3, 0, 4, '27, 30, 27, 30 mins'),
					      (0, 4, 0, 3, '20, 20, 20 mins'),
					      (1, 4, 0, 4, '35, 40, 30, 45 mins'),
					      (0, 2, 1, 3, '12, 15, 12 mins'),
					      (1, 2, 1, 4, '20, 22, 20, 22 mins'),
					      (0, 3, 1, 3, '15, 20, 15 mins'),
					      (1, 3, 1, 4, '25, 27, 25, 27 mins'),
					      (0, 4, 1, 3, '20, 20, 20 mins'),
					      (1, 4, 1, 4, '30, 35, 30, 35 mins');