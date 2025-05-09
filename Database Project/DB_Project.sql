create database Bank_Managment_System_Project;
use Bank_Managment_System_Project;

-- Creating table for customers
create table customers (
	customer_id int primary key auto_increment,
    name varchar(100),
    email varchar(150) unique,
    phone varchar(20) unique
);

-- Creating table for accounts  
 create table accounts (
 account_id int primary key auto_increment,
 customer_id int,
 balance decimal(10,2) default 0,
 account_type enum ('Savings','Checking'),
 foreign key (customer_id) references customers (customer_id)
 );
 
 -- Creating Table for Transactions
 create table transactions (
 transaction_id int primary key auto_increment,
 account_id int,
 amount decimal(10,2),
 type enum ('Deposit','Withdrawl'),
 transaction_time datetime default current_timestamp,
 foreign key (account_id) references accounts (account_id)
 );
 
--  Creating table for Staff Users
 create table users (
 user_id int primary key auto_increment,
 username varchar(100) unique,
 password varchar(200),
 role enum('Admin','Teller','Manager')
 );
 
--  Creating procedure to insert customer
 delimiter $$
 create procedure InsertCustomer (in cust_name varchar(100) , in e_mail varchar(150) , in phone_number varchar (20))
 begin
	declare exit handler for sqlexception
    begin
		select 'This email or phone number is already taken' as STATUS;
	end;
    if e_mail like '%@gmail.com' then
		insert into customers (name,email,phone)
		values (cust_name,e_mail,phone_number);
        select 'Customer added succesfully' as STATUS;
	else
		select 'Invalid email' as STATUS;
	end if;
end$$


--  Creating procedure to insert account
delimiter $$
create procedure InsertAccount (in cust_id int, in bal int ,in type varchar(20))
begin
	declare exit handler for sqlexception
    begin
		select 'Invalid customer ID , balance or type' as STATUS;
	end;
    insert into accounts (customer_id,balance,account_type)
    values (cust_id,bal,type);
    select 'Account added successfully' as STATUS;
end$$

--  Creating function to get balance of an account
delimiter $$
create function getBalance (acc_id int)
returns decimal(10,2)
deterministic
begin
	declare bal decimal(10,2);
	select balance into bal from accounts where account_id = acc_id;
    return bal;
end$$

--  Creating procedure to insert transactions
delimiter $$
create procedure InsertTransactions (in acc_id int, in amo int ,in t_type varchar(20))
begin
	declare bal decimal(10,2);
	declare exit handler for sqlexception
    begin
		select 'Invalid account ID , amo or type';
	end;
    set bal = getBalance(acc_id);
    if ( t_type = 'Deposit' and amo > 0 ) or ( t_type = 'Withdrawl' and amo <= bal and amo > 0) then
		insert into transactions (account_id,amount,type)
		values (acc_id,amo,t_type);
		select 'Transaction completed successfully' as STATUS;
	else
		select 'Enter a valid amount' as STATUS;
	end if;
end$$



--  Creating trigger to update account after transaction
delimiter $$
create trigger update_account
after insert 
on transactions
for each row
begin
	if new.type = 'Deposit' then
		update accounts
        set balance = balance + new.amount
        where account_id = new.account_id;
	else
		update accounts
        set balance = balance - new.amount
        where account_id = new.account_id;
	end if;
end $$

--  Creating procedure to insert staff user
delimiter $$
create procedure InsertUser (in user_name varchar(100) , in pass varchar(200) , in rol varchar(20))
begin
	declare exit handler for sqlexception
    begin
		select 'An error occured during insertion' as STATUS;
	end;
    insert into users ( username,password,role)
    values (user_name,pass,rol);
    select 'User inserted Successfully' as STATUS;
end$$

--  Creating procedure for Login System
delimiter $$
create procedure LoginSystem (in user_name varchar(100), in pass varchar(200))
begin
	declare user_role varchar(20);
	declare exit handler for sqlexception
    begin
		select 'Enter username of 100 characters  and password of 200 chracters' as STATUS;
	end;
    select role into user_role from users where username = user_name and password = pass;
    if user_role is not null then
		select 'Login Successfull' as STATUS;
	else
		select 'Login Failed. Invalid username or password' as STATUS;
	end if;
end$$

call InsertUser('Basit123','123abc','Manager');

call LoginSystem('Basit123','123abc');

--  Creating view to view total accounts of each customer
create view View_Total_Accounts_Customer as
select c.name , c.email , count(a.account_id) as Total_Accounts
from customers c left join accounts a
on c.customer_id = a.customer_id
group by a.customer_id , c.name , c.email;

--  Creating procedure to transfer amount from one account to another
delimiter $$
create procedure TransferAccount(in from_acc int , in to_acc int , in amo int)
begin
	declare from_bal decimal(10,2);
	declare exit handler for sqlexception
    begin
		select 'Enter valid account number or amount' as STATUS;
	end;
    set from_bal = getBalance(from_acc);
    if amo <= from_bal and amo > 0 then
		call InsertTransactions(from_acc,amo,'Withdrawl');
        call InsertTransactions(to_acc,amo,'Deposit');
        select 'Money transferred successfully' as STATUS;
	else
		select 'Enter a valid amount' as STATUS;
	end if;
end$$

--  Creating view to view account summary
create view AccountSummary as
select a.account_id , c.name , a.balance , a.account_type
from customers c inner join accounts a
on c.customer_id = a.customer_id;  

select * from AccountSummary;

call TransferAccount(1,2,1000);
select * from View_Total_Accounts_Customer;

call InsertTransactions(3,2000,'Deposit');


 
 
