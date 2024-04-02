CREATE OR REPLACE EXTERNAL TABLE `{{ bq_table_name_platforms }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ gcs_bucket_name }}/platforms/*.parquet']
);