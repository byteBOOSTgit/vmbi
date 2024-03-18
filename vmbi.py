import pandas as pd
import os
# vmbi.py: Uses a master inventory file and checks whether the inventory was scanned by a scan result file.  
# The resulting report indicates which scan reports the inventory item (computer) showed up in.
# The user can determine whether a item in inventory was ever scanned or if the scanner missed it.

# inventory file should be in csv format
inventory_filename = r"absolute-path-to-inventory-file"
scan_files_dir = r"absolute-path-to-scan-files-dir"
# the inventory structure is the master inventory stucture that will be populated with scan results
inventory = pd.read_csv(inventory_filename)
scan_files = os.listdir(scan_files_dir)
# iterate through scan files, to normalize the host name found in the scan result
# then add a column for the scan date, set the value to true if the asset name in the scan is found in the inventory
for file_name in scan_files:
    if file_name.endswith(".csv"):
        # read in the scan file
        scan = pd.read_csv(os.path.join(
            scan_files_dir, file_name), low_memory=False)
        # customize based on file naming convention
        tokens = file_name.split("_")
        # add column for scan date assuming scan_date is the second token in the file name
        scan_date = tokens[1]
        scan['Scan Date'] = scan_date
        # default to None, update with asset name if found in inventory
        scan['Asset Name'] = None
        # iterate through scan results, to normalize the host name found in the scan result
        for index, row in scan.iterrows():
            temp_name = row["NetBIOS Name"]
            # if not empty, default to IP Address
            if str(row["NetBIOS Name"]) == "nan":
                temp_name = row["DNS Name"]
                # if temp_name is still empty, default to IP Address
                if temp_name == "nan":
                    temp_name = row["IP Address"]
            # normalize the host name to match the hostname naming convention that is in the inventory
            #temp_name = temp_name.lower().replace(" ", "-").replace("_", "-").replace(".", "-")
            # replace the Asset Name with tne normalize hostname in temp_name
            scan.iloc[index, scan.columns.get_loc("Asset Name")] = temp_name.upper()
            # standardizing upper case for hostnames
            inventory["Name"] = inventory["Name"].apply(str.upper) 
            # add a column named for the scan date, set the value to true if the asset name in the scan is found in the inventory
            inventory[scan_date] = inventory["Name"].isin(scan["Asset Name"])
