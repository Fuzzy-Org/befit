DROP TABLE IF EXISTS LowCarb;

CREATE TABLE if not exists LowCarb (
	Calories int not null,
    Nutrition varchar(255),
    Breakfast varchar(255),
    Lunch varchar(255),
    Dinner varchar(255),
    primary key (Calories)
);

INSERT INTO LowCarb VALUES (800, '800;52.5;22.8;97.2', '277:69x1;57x1', '221:21x1;70x2.5', '302:11x0.5;28x1'),
						   (1000, '1000;94.3;43.7;64.7', '341:07x1;08x1', '264:09x1;10x0.5', '395:11x1;04x1'),
                           (1200, '1200;74.4;63.1;91.2', '375:71x1;02x1', '375:34x2;70x6', '450:72x1;28x1'),
                           (1400, '1400;80.3;65.7;126.6', '430:73x1;74x1.5', '420:75x0.5;76x1', '550:77x2.5;70x8'),
                           (1600, '1600;94.8;72.3;146.4', '436:20x2;08x3', '443:21x1;22x4', '721:23x1.5;14x2'),
                           (1800, '1800;107.1;92.4;149.4', '529:78x2;08x2', '531:21x2.5;14x2', '740:79x3;80x1'),
                           (2000, '2000;126.1;84.6;188.8', '550:29x3;13x2', '530:30x1;22x2', '920:31x4;32x1'),
                           (2200, '2200;135.1;99.2;203.3', '579:33x2;13x2', '840:34x3;32x1', '784:35x2;28x1');