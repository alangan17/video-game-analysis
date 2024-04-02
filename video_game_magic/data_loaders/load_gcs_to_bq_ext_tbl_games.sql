CREATE OR REPLACE EXTERNAL TABLE `{{ bq_table_name_games }}`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://{{ gcs_bucket_name }}/games/*.parquet']
);