CREATE OR REPLACE EXTERNAL TABLE `{{ bq_table_name_parent_platforms }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ gcs_bucket_name }}/parent_platforms/*.parquet']
);