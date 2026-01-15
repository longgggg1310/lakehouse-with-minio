# Please refer to the following documentation for more information
# about Delta Lake: https://delta-io.github.io/delta-rs/python/usage.html
from deltalake import DeltaTable
from helpers import load_cfg

CFG_FILE = "./utils/config.yaml"


def main():
    cfg = load_cfg(CFG_FILE)
    fake_data_cfg = cfg["fake_data"]

    # Load Delta Lake table
    print("*" * 80)
    dt = DeltaTable(fake_data_cfg["folder_path"])
    # Uncomment the below line to switch to another version
    dt.load_version(0)
    print("[INFO] Loaded Delta Lake table successfully!")

    # Investigate Delta Lake table
    print("*" * 80)
    print("[INFO] Delta Lake table schema:")
    print(dt.schema().json())
    print("*" * 40)
    print("[INFO] Delta Lake table's current version:")
    print(dt.version())
    print("*" * 40)
    print("[INFO] Delta Lake files:")
    print(dt.files())
    print("*" * 40)

    # Query some data
    print("[INFO] Delta Lake table data on pressure column:")
    print(dt.to_pandas(columns=["pressure"]))
    print("*" * 40)

    # Investigate history of actions performed on the table
    print("[INFO] History of actions performed on the table")
    print(dt.history())
    print("*" * 40)


if __name__ == "__main__":
    main()
