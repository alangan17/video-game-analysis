CREATE OR REPLACE EXTERNAL TABLE `{{ bq_table_name_stores }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ gcs_bucket_name }}/stores/*.parquet']
);