CREATE OR REPLACE EXTERNAL TABLE `{{ bq_table_name_tags }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ gcs_bucket_name }}/tags/*.parquet']
);