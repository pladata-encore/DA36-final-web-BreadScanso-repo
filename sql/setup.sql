# root계정으로 실행

# bsdb 생성
create database bsdb character set utf8mb4 collate utf8mb4_unicode_ci;

# breadscanso사용자에게 bsdb 권한 부여
grant all privileges on bsdb.* to 'breadscanso'@'%';
