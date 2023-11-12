CREATE TABLE `Account` (
  `account_id` int NOT NULL,
  `account_num` varchar(14) NOT NULL,
  `account_type` varchar(7) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `balance` int NOT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Customer` (
  `email` varchar(25) NOT NULL,
  `name` varchar(50) NOT NULL,
  `passwords` varchar(50) NOT NULL,
  `login_time` time NOT NULL,
  `login_date` date NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `linkAccountTransaction` (
  `transaction_id` int NOT NULL,
  `from_account` int NOT NULL,
  `to_account` int NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `from_account` (`from_account`),
  KEY `to_account` (`to_account`),
  CONSTRAINT `linkaccounttransaction_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `Transaction` (`transaction_id`),
  CONSTRAINT `linkaccounttransaction_ibfk_2` FOREIGN KEY (`from_account`) REFERENCES `Account` (`account_id`),
  CONSTRAINT `linkaccounttransaction_ibfk_3` FOREIGN KEY (`to_account`) REFERENCES `Account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `linkCustomerAccount` (
  `account_id` int NOT NULL,
  `email` varchar(25) NOT NULL,
  PRIMARY KEY (`account_id`),
  KEY `email` (`email`),
  CONSTRAINT `linkcustomeraccount_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Customer` (`email`),
  CONSTRAINT `linkcustomeraccount_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `Account` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Transaction` (
  `transaction_id` int NOT NULL,
  `amount` int NOT NULL,
  `trans_time` time NOT NULL,
  `trans_date` date NOT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;