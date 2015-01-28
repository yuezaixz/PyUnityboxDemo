drop table if exists orders;
create table orders (
  id integer primary key autoincrement,
  product_name text not null,
  consignee_name text not null,
  otp_phone_number text not null,
  consignee_email text not null,
  pickuppoint text not null,
  extra_code text not null,
  remark text not null,
  serial_number text not null
);