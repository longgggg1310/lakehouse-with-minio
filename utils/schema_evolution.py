# Reference: https://delta.io/blog/2023-02-08-delta-lake-schema-evolution/
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def main():
    # The entrypoint to access all functions of Spark
    builder = (
        SparkSession.builder.master("local[*]")
        .appName("Python Spark stop word example")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    # Declare the 1st dataframe with more columns,
    # then write it to the delta lake table format
    df1 = spark.createDataFrame([(10, 20, 30), (11, 21, 31)])\
        .toDF(
            "humidity", "velocity", "temperature"
        )
    df1.write.format("delta").save("tmp/iot_data")
    # Write the second dataframe, notice that, you must use
    # .mode("append"), if not you will meet an error indicating data existed
    df2 = spark.createDataFrame([(12, 22), (13, 23)])\
        .toDF("humidity", "velocity")
    df2.write.format("delta").mode("append").save("tmp/iot_data")
    # Show the data, now you should see 2 dataframe have been merged
    # note that, parquet also provides schema evolution, please 
    # read more at https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#schema-merging
    spark.read.format("delta").load("tmp/iot_data").show()


if __name__ == "__main__":
    main()
