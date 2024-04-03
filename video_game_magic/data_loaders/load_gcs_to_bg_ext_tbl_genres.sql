CREATE OR REPLACE EXTERNAL TABLE `{{ bq_table_name_genres }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ gcs_bucket_name }}/genres/*.parquet']
);