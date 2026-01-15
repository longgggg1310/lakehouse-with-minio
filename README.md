# lakehouse-with-minio

Nền tảng Lakehouse hiện đại xây dựng trên MinIO (S3-compatible object storage), Delta Lake (open table format), Hive Metastore (catalog) và Trino (distributed SQL engine).

Project này minh hoạ cách xây dựng một data platform cloud-native, trong đó Data Lake có thể được query như Data Warehouse.

---

## Tổng quan

Repository này triển khai một kiến trúc Lakehouse tối giản gồm:

- **MinIO** làm object storage (tương thích S3) cho Data Lake  
- **Parquet** làm định dạng lưu trữ vật lý  
- **Delta Lake** làm open table format cung cấp ACID-like semantics, versioning và time travel  
- **Hive Metastore** làm metadata catalog  
- **Trino** làm SQL query engine phân tán  

Demo sử dụng dataset giao dịch bán lẻ (retail transactions) và minh hoạ quy trình ingest dữ liệu vào Delta table và query bằng SQL.

---

## Kiến trúc

```text
        SQL
         |
       Trino
         |
 Hive Metastore (catalog)
         |
     Delta Lake
         |
      MinIO (S3)
```

---

## Các khái niệm chính

- Object Storage làm Data Lake (MinIO / S3)
- Parquet làm columnar storage format
- Delta Lake làm open table format (transaction log, versioning)
- Hive Metastore làm catalog service
- Trino làm distributed SQL engine

---

## Mục tiêu

Minh hoạ cách xây dựng một data platform hiện đại hoàn toàn bằng open-source, và cách một Data Lake có thể được sử dụng như một Data Warehouse thông qua kiến trúc Lakehouse.


## Hướng dẫn sử dụng (How-to Guide)

### Dựng infra
```shell
docker compose -f docker-compose.yml -d
```
### Sinh dữ liệu

```shell
python utils/write_delta_table.py
```

### Tải dữ liệu lên Minio

```shell
python utils/upload_data_to_datalake.py
```

Sau khi upload, dữ liệu sẽ nằm tại:
```shell
s3://sales/orders/
  ├── _delta_log/
  ├── part-00000.parquet
```

### Tải dữ liệu lên Minio
Tìm hiểu Delta Lake
Để hiểu rõ hơn cách Delta Lake hoạt động, hãy đọc comment trong file:

```shell
utils/investigate_delta_table.py
```
và chạy:
```shell
python utils/investigate_delta_table.py
```

Đừng quên cài đặt các thư viện cần thiết trong file `requirements.txt` trước khi chạy các script:
```shell
pip install -r requirements.txt
```

### Tạo schema và register bảng trong Trino
Sau khi dữ liệu đã được upload lên MinIO, hãy truy cập vào container Trino bằng lệnh:
```shell
docker exec -ti datalake-trino bash
```

Sau đó chạy Trino ở chế độ interactive:
```shell
trino
```

Tạo schema và bảng 
```shell
CREATE SCHEMA IF NOT EXISTS lakehouse.sales
WITH (location = 's3://sales/');

CREATE TABLE IF NOT EXISTS lakehouse.sales.retail_transactions (
  order_id VARCHAR,
  order_time TIMESTAMP(3),
  customer_id VARCHAR,
  product_id VARCHAR,
  quantity BIGINT,
  price DOUBLE,
  country VARCHAR
) WITH (
  location = 's3://sales/orders'
);
```