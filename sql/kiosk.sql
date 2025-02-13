use bsdb;

START TRANSACTION;
INSERT INTO bsdb.kiosk_orderinfo (order_id, order_datetime, total_price, earned_points, store) VALUES ();


COMMIT;
ROLLBACK; # 위 DML 실행중 오류가 발생한 경우